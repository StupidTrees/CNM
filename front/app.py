import base64
import io
import os
import random

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import numpy as np
from dash import dcc, ctx
from dash import html
from dash import Dash
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from dash.long_callback import DiskcacheManager

import utils.config
from backend.process import generate_novel_graph
from front.adapter import graph_to_view
from front.view_model import ViewModel

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

import diskcache

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, external_stylesheets=external_stylesheets)
viewModel = ViewModel()
cards = [
    dbc.Card(
        [
            html.H3("0", className="card-title", id="connected_component_num"),
            html.P("连通分量数", className="card-text"),
        ],
        body=True,
        inverse=True,
        color="primary",
    ),
    dbc.Card(
        [
            html.H3(f"{0:.2f}", className="card-title", id="avg_degree"),
            html.P("平均结点度数", className="card-text"),
        ],
        body=True,
        color="light",
    ), dbc.Card(
        [
            html.H3(f"{0:.2f}", className="card-title", id="avg_path_len"),
            html.P("平均路径长度", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ), dbc.Card(
        [
            html.H3(f"{0:.2f}", className="card-title", id="cluster_co"),
            html.P("聚类系数", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ), dbc.Card(
        [
            html.H3(f"{0:.2f}", className="card-title", id="coreness"),
            html.P("Coreness", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    )
]
panel = dbc.Card(
    [
        html.H5("书籍"),
        dcc.Dropdown(
            id="window-dropdown",
            options=[
                {"label": name, "value": value} for name, value in zip(viewModel.names, viewModel.keys)
                # {"label": "红楼梦", "value": "red"},
                # {"label": "三国演义", "value": "kingdom"},
                # {"label": "西游记", "value": "west"},
                # {"label": "水浒传", "value": "who"},
            ],
            value="red",
            clearable=False,
            style={"padding": "20 20 20 20"}
        ),
        html.Br(),
        dcc.Upload([
            '拖拽或',
            html.A('选择小说txt文件')
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        }, id='upload', multiple=False),
        html.Div(id="upload-result"),
        dbc.Spinner(html.Div(id="loading-output"), color="primary"),
        dbc.Collapse(
            dbc.Row(
                [dbc.Col(dbc.Button('进行分析', id='add_graph', color='primary'), width=3),
                 dbc.Col(dbc.Button('取消', id='upload_cancel', color='light'), width=3),
                 ]
            ), id="upload-buttons", is_open=False
        ),
        dbc.Label('', id='upload-label')
        ,

    ], body=True
)

view_panel = dbc.Card(
    body=True,
    children=[
        html.H5("显示"),
        html.Br(),
        dbc.Label("布局"),
        dbc.RadioItems(
            className="inline",
            id="layout-radio",
            options=[
                {"label": "COSE", "value": "cose"},
                {"label": "中心", "value": "concentric"},
                {"label": "环状", "value": "circle"},
                {"label": "宽度", "value": "breadthfirst"},
                # {"label": "随机", "value": "random"},
                {"label": "网格", "value": "grid"},
            ],
            labelStyle={
                "display": "inline-block",
                "margin": "2px",
            },
            value="concentric",
            inline=True
        ),
        html.Br(), html.Br(),
        dbc.Label(id="degree-slider-label", children="按度数筛选节点:"),
        dcc.RangeSlider(
            id="degree-slider",
            min=0,
            max=400,
            value=[0, 500],
            step=5,
            marks={
                str(int(x)): str(int(x))
                for x in np.linspace(0, 500, 5)
            },
        )
    ]

)

attack_panel = dbc.Card([html.H5("攻击"),
                         html.Br(), dbc.Row(
        [dbc.Col(dbc.Button('随机攻击', id='random-attack'), width=3),
         dbc.Col(dbc.Button('意图攻击', id='intentional-attack', color='warning'), width=3),
         dbc.Col(dbc.Button('复原', id='reset', color='success', n_clicks=0), width=3),
         dbc.Label('已删除', id='ia-label'),
         ]
    )], body=True)

categories_panel = dbc.Card([html.H5("结点类别"),
                             html.Br(), html.Span(id='nodes_category')], body=True)


def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
    logo = html.Img(
        src=app.get_asset_url("dash-logo.png"), style={"float": "right", "height": 60}
    )
    link = html.A(logo, href="https://plotly.com/dash/")

    return dbc.Row([dbc.Col(title, md=8), dbc.Col(link, md=4)])


app.layout = dbc.Container(
    [
        Header("小说人物关系分析系统", app),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [panel, view_panel, attack_panel, categories_panel], width=3,
                ),
                dbc.Col([
                    dbc.Row(
                        [dbc.Col(card) for card in cards]
                    ),
                    cyto.Cytoscape(
                        id='cytoscape',
                        elements=[],
                        layout={'name': 'concentric'},
                        style={'width': '100%', 'height': '1000px'},
                        stylesheet=[],
                        responsive=True
                    )
                    ,
                    dbc.Toast(
                        id="node_selection_toast",
                        header="点击以选中结点",
                        is_open=False,
                        dismissable=False,
                        # icon="primary",
                        children=[html.Div(
                            [dbc.Row([dbc.Col(dbc.Label(id="ia-selected-label"), width=6),
                                      dbc.Col(dbc.ButtonGroup(
                                          [dbc.Button('取消', color='dark', id='ia-cancel'),
                                           dbc.Button('删除', color='primary', id='ia-delete')]), width=3)
                                      ]),
                             dbc.ListGroup(id='selected_nodes')]
                        )
                        ],
                        # top: 66 positions the toast below the navbar
                        style={"position": "fixed", "top": 256, "left": 360, "width": 220},
                    )], width=9),
            ]
        ),
        dbc.Col([
            dbc.Row([dbc.Col(dcc.Graph(id='popular_nodes'))
                        , dbc.Col(dcc.Graph(id='coreness_nodes'))
                     ]),
            dbc.Row([dbc.Col(dcc.Graph(id='degree_distribution')),dbc.Col(dcc.Graph(id='cluster_nodes'))]),
        ]),
        dbc.Toast(
            id="popover",
            is_open=False,
            # dismissable=True,
            # duration=500,
            # icon="primary",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "bottom": 10, "right": 10, "width": 200},
        ),
        html.Div(id="temp"),
    ],
    fluid=True,
)


# app.layout = html.Div(
#     className="page",
#     children=[
#         html.Div(
#             className="sub_page",
#             children=[
#                 # html.Div(className='col-2'),
#                 html.Div(
#                     children=[
#                         html.H3(
#                             className="product",
#                             children=[
#                                 "名著人物关系图"
#                             ],
#                         ),
#                         panel,
#                         dbc.Row(
#                             [dbc.Col(card) for card in cards]
#                         ),
#                         charts
#                     ]
#                 ),
#             ],
#         )
#     ],
# )


@app.callback(
    Output("degree-slider-label", "children"),
    Input("degree-slider", "value")
)
def update_label(degree_range):
    return "按度数筛选节点：{}-{}".format(degree_range[0], degree_range[1])


@app.callback(
    Output('node_selection_toast', 'is_open'),
    Output("random-attack", "disabled"),
    Output("intentional-attack", "disabled"),
    Output("reset", "disabled"),
    Input("ia-label", "children"),
    Input("intentional-attack", "n_clicks"),
    Input("ia-cancel", "n_clicks"),
    Input("reset", "n_clicks"),
)
def intentional_attack(x, a, b, d):
    triggered_id = ctx.triggered_id
    label = ""
    if triggered_id == 'reset':
        viewModel.is_ia = False
        viewModel.ia_selected = []
    elif triggered_id == 'intentional-attack':
        viewModel.is_ia = True
        viewModel.ia_selected = []
    elif triggered_id == 'ia-cancel':
        viewModel.is_ia = False
        viewModel.ia_selected = []
    return viewModel.is_ia, viewModel.is_ia, viewModel.is_ia, label


@app.callback(
    Output("cytoscape", "elements"),
    Output("connected_component_num", "children"),
    Output("avg_degree", "children"),
    Output("avg_path_len", "children"),
    Output("cluster_co", "children"),
    Output("coreness", "children"),
    Output("nodes_category", "children"),
    Output("popular_nodes", "figure"),
    Output("coreness_nodes", "figure"),
    Output("degree_distribution", "figure"),
    Output("cluster_nodes", "figure"),
    Output('ia-label', 'children'),
    Input("window-dropdown", "value"),
    Input("degree-slider", "value"),
    Input('random-attack', 'n_clicks'),
    Input('ia-delete', 'n_clicks'),
    Input('reset', 'n_clicks')
)
def update_figure(book, degree_range, random_attack_click, reset_click, ia_label):
    triggered_id = ctx.triggered_id
    graph = viewModel.get_graph(book, triggered_id == 'reset')
    if triggered_id == 'random-attack':
        nodes = random.sample(graph.nodes, int(len(graph.nodes) * 0.3))
        graph.remove_nodes([node.id for node in nodes])
        # graph.calc_cluster_coefficient()
        # graph.calc_coreness()
        graph.calc_connected_components_num()
    if triggered_id == 'ia-delete' and len(viewModel.ia_selected) > 0:
        graph.remove_nodes(viewModel.ia_selected)
        viewModel.ia_selected = []
        viewModel.is_ia = False
        graph.calc_connected_components_num()
        # graph.calc_cluster_coefficient()
        # graph.calc_coreness()
    ss, e = graph_to_view(graph, degree_range)
    cn = graph.get_low_cluster_nodes()
    cluster = go.Figure(
        data=[go.Bar(x=[n.id for n, _ in cn], y=[ce for _, ce in cn])],
        layout_title_text="人物聚类系数"
    )
    dd = graph.get_degree_distribution()
    degree_dis = go.Figure(
        data=[go.Bar(x=list(dd.keys()), y=list(dd.values()))],
        layout_title_text="度数分布"
    )
    pn = graph.get_popular_nodes()
    popular = go.Figure(
        data=[go.Bar(x=[n.id for n, _ in pn], y=[degree for _, degree in pn])],
        layout_title_text="人物度数"
    )

    con = graph.get_high_coreness_nodes()
    coreness = go.Figure(
        data=[go.Bar(x=[n.id for n, _ in con], y=[degree for _, degree in con])],
        layout_title_text="人物Coreness"
    )

    nodes_cate = []
    for k, v in graph.get_node_color_map().items():
        nodes_cate.append(
            dbc.Badge(k, color=v, pill=True, className="me-1", style={"margin": "4 4 4 4"}, text_color="white")
        )
    return e, "{}".format(graph.get_connected_component_num()), "{:.2f}".format(
        graph.get_average_degree()), "{:.2f}".format(
        graph.get_average_path_length()), "{:.2f}".format(
        graph.get_cluster_coefficient()), "{:.2f}".format(graph.get_coreness()), \
           nodes_cate, popular, coreness, degree_dis,cluster, ""


@app.callback(
    Output("cytoscape", "stylesheet"),
    Input("window-dropdown", "value"),
    Input("degree-slider", "value")
)
def update_style(book, degree_range):
    ss, e = graph_to_view(viewModel.get_graph(book, False), degree_range)
    return ss


@app.callback(
    Output("cytoscape", "layout"),
    Input("layout-radio", "value")
)
def update_layout(type):
    layout = {}
    if type == 'cose':
        layout = {
            'idealEdgeLength': 200,
            'refresh': 20,
            'fit': True,
            'padding': 30,
            'randomize': False,
            'animate': False,
            'componentSpacing': 200,
            'nodeRepulsion': 20000000,
            'nodeOverlap': 500,
            'edgeElasticity': 200,
            'nestingFactor': 5,
            'gravity': 80,
            'numIter': 1000,
            'initialTemp': 300,
            'coolingFactor': 0.99,
            'minTemp': 1.0
        }
    layout["name"] = type
    return layout


@app.callback(Output('selected_nodes', 'children'),
              Output("ia-selected-label", "children"),
              Input('cytoscape', 'selectedNodeData'))
def display_selection(data_list):
    label = "未选择结点"
    if data_list is None or not viewModel.is_ia:
        return [], label
    cities_list = [dbc.ListGroupItem(data['label'], color="info") for data in data_list]
    viewModel.ia_selected = [data['label'] for data in data_list]

    if len(cities_list) > 0:
        label = "选中{}个结点".format(len(cities_list))
    return cities_list, label


@app.callback(Output('popover', 'is_open'),
              Output('popover', 'children'),
              [Input('cytoscape', 'mouseoverNodeData')],
              )
def display_hover_node(data):
    if data:
        node_id = data['id']
        graph = viewModel.current_graph
        node = graph.id2nodes[node_id]
        content = [
            dbc.ListGroupItem([html.Label("{}".format(data['label']), style={"color": "white"})],
                              color=graph.get_node_color_map()[data['class_name']]),
            dbc.ListGroupItem("度数：{}".format(node.get_degree()))
        ]
        if node in graph.cluster_coefficient.keys():
            content.append(dbc.ListGroupItem("聚类系数：{}".format(graph.cluster_coefficient[node])))
        if node in graph.coreness.keys():
            content.append(dbc.ListGroupItem("Coreness：{}".format(graph.coreness[node])))
        return True, content
    return False, []


@app.callback(
    Output("upload-label", "children"),
    Output("window-dropdown", "options"),
    Output("window-dropdown", "value"),
    Input('add_graph', 'n_clicks'),
    background =True,
    prevent_initial_call=True,
    running=[
        (Output("add_graph", "disabled"), True, False),
        (Output("loading-output", "children"), "导入并建模中...需要点时间", "导入完成"),
    ], manager=background_callback_manager)
def add_graph(a):
    key = viewModel.upload_key
    dir = utils.config.raw_path + viewModel.upload_key + "/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(utils.config.raw_path + "{}/{}.txt".format(viewModel.upload_key, viewModel.upload_key), "w+") as f:
        f.write(viewModel.upload_content)
    if os.path.exists('backend/model/cache/{}.pkl'.format(key)):
        os.remove('backend/model/cache/{}.pkl'.format(key))
    generate_novel_graph(key)
    viewModel.add_graph(key)
    viewModel.upload_content = None
    viewModel.upload_key = None
    viewModel.ready_upload = False
    return "", [{"label": name, "value": value} for name, value in zip(viewModel.names, viewModel.keys)], key


@app.callback(
    Output('upload-buttons', 'is_open'),
    Output('upload-result', 'children'),
    Input('upload', 'contents'),
    Input('upload_cancel', 'n_clicks'),
    Input('upload-label', 'children'),
    State('upload', 'filename'))
def update_output(list_of_contents, upload_cancel, upload_label, list_of_names):
    trigger_id = ctx.triggered_id
    if trigger_id == 'upload_cancel' or trigger_id == 'upload-label':
        viewModel.upload_content = None
        viewModel.ready_upload = False
        return False, ""
    elif trigger_id == "upload" and list_of_contents is not None:
        return parse_contents(list_of_contents, list_of_names)
    return viewModel.ready_upload, ""


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    contents = ""
    key = filename.split(".")[0]
    try:
        for line in io.StringIO(decoded.decode('utf-8')).readlines():
            contents += line
        viewModel.upload_content = contents
        viewModel.ready_upload = True
        viewModel.upload_key = key
    except Exception:
        viewModel.ready_upload = False
        return False, html.Div([
            'There was an error processing this file.'
        ])
    return True, html.Div([
        html.H5(key),
        html.Pre(contents[0:100] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
