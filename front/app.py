import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import numpy as np
from dash import dcc
from dash import html
from dash import Dash
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from front.adapter import graph_to_view
from front.view_model import red_graph, kingdom_graph, west_graph, who_graph

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
######## ## the APP


cards = [dbc.Card(
    [
        html.H2(f"{0:.2f}", className="card-title", id="avg_degree"),
        html.P("平均结点度数", className="card-text"),
    ],
    body=True,
    color="light",
), dbc.Card(
    [
        html.H2(f"{0:.2f}", className="card-title", id="avg_path_len"),
        html.P("平均路径长度", className="card-text"),
    ],
    body=True,
    color="dark",
    inverse=True,
), dbc.Card(
    [
        html.H2(f"{0:.2f}", className="card-title", id="cluster_co"),
        html.P("聚类系数", className="card-text"),
    ],
    body=True,
    color="dark",
    inverse=True,
), dbc.Card(
    [
        html.H2(f"{0:.2f}", className="card-title", id="coreness"),
        html.P("Coreness", className="card-text"),
    ],
    body=True,
    color="dark",
    inverse=True,
)
]
panel = html.Div(
    className="row",
    children=[
        html.Div(
            className="col-4",
            children=[
                html.Label("选择名著: "),
                dcc.Dropdown(
                    id="window-dropdown",
                    options=[
                        {"label": "红楼梦", "value": "red"},
                        {"label": "三国演义", "value": "kingdom"},
                        {"label": "西游记", "value": "west"},
                        {"label": "水浒传", "value": "who"},
                    ],
                    value="red",
                ),
                html.Label("布局:  ", className="inline"),
                dcc.RadioItems(
                    className="inline",
                    id="layout-radio",
                    options=[
                        {"label": "COSE", "value": "cose"},
                        {"label": "中心", "value": "concentric"},
                        {"label": "环状", "value": "circle"},
                        {"label": "宽度", "value": "breadthfirst"},
                        {"label": "随机", "value": "random"},
                        {"label": "网格", "value": "grid"},
                    ],
                    value="cose",
                    labelStyle={
                        "display": "inline-block",
                        "margin": "6px",
                    },
                ),
                html.Label(id="degree-slider-label", children="按度数筛选节点:"),
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
                ),
            ],
        )
    ],
)
charts = html.Div(
    [
        cyto.Cytoscape(
            id='cytoscape',
            elements=[],
            layout={'name': 'concentric'},
            style={'width': '100%', 'height': '1000px'},
            stylesheet=[],
            responsive=True
        )

        , dcc.Graph(id='popular_nodes')
        , dcc.Graph(id='coreness_nodes')
        , dcc.Graph(id='cluster_nodes')
        ,dcc.Markdown(id='cytoscape-selectedNodeData-markdown')
    ]
)
app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="sub_page",
            children=[
                # html.Div(className='col-2'),
                html.Div(
                    children=[
                        html.H3(
                            className="product",
                            children=[
                                "名著人物关系图"
                            ],
                        ),
                        panel,
                        dbc.Row(
                            [dbc.Col(card) for card in cards]
                        ),
                        charts
                    ]
                ),
            ],
        )
    ],
)


@app.callback(
    Output("degree-slider-label", "children"),
    Input("degree-slider", "value")
)
def update_label(degree_range):
    return "按度数筛选节点：{}-{}".format(degree_range[0], degree_range[1])


@app.callback(
    Output("cytoscape", "elements"),
    Output("avg_degree", "children"),
    Output("avg_path_len", "children"),
    Output("cluster_co", "children"),
    Output("coreness", "children"),
    Output("popular_nodes", "figure"),
    Output("coreness_nodes", "figure"),
    Output("cluster_nodes", "figure"),
    Input("window-dropdown", "value"),
    Input("degree-slider", "value")
)
def update_figure(book, degree_range):
    graph = None
    if book == 'red':
        graph = red_graph
    elif book == 'kingdom':
        graph = kingdom_graph
    elif book == 'west':
        graph = west_graph
    elif book == 'who':
        graph = who_graph
    ss, e = graph_to_view(graph, degree_range)
    cn = graph.get_low_cluster_nodes()
    cluster = go.Figure(
        data=[go.Bar(x=[n.id for n, _ in cn], y=[ce for _, ce in cn])],
        layout_title_text="人物聚类系数"
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
    return e, "{:.2f}".format(graph.get_average_degree()), "{:.2f}".format(
        graph.get_average_path_length()), "{:.2f}".format(
        graph.get_cluster_coefficient()), "{:.2f}".format(graph.get_coreness()), popular, coreness, cluster


@app.callback(
    Output("cytoscape", "stylesheet"),
    Input("window-dropdown", "value"),
    Input("degree-slider", "value")
)
def update_style(book, degree_range):
    global ss
    if book == 'red':
        ss, e = graph_to_view(red_graph, degree_range)
    elif book == 'kingdom':
        ss, e = graph_to_view(kingdom_graph, degree_range)
    elif book == 'west':
        ss, e = graph_to_view(west_graph, degree_range)
    elif book == 'who':
        ss, e = graph_to_view(who_graph, degree_range)
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


@app.callback(Output('cytoscape-selectedNodeData-markdown', 'children'),
              Input('cytoscape', 'selectedNodeData'))
def display_selection(data_list):
    if data_list is None:
        return "nothing"

    cities_list = [data['label'] for data in data_list]
    return "You selected the following cities: " + "\n* ".join(cities_list)