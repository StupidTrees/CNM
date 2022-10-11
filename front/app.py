import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import dcc
from dash import html
from dash import Dash
from dash.dependencies import Output, Input

from front.adapter import graph_to_view
from front.view_model import red_graph, kingdom_graph, west_graph, who_graph

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

app = Dash(__name__,external_stylesheets = external_stylesheets)
dt = 1
t_max = 100
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
                        {"label": "中心", "value": "concentric"},
                        {"label": "环状", "value": "circle"},
                        {"label": "宽度", "value": "breadthfirst"},
                        {"label": "随机", "value": "random"},
                        {"label": "网格", "value": "grid"},
                    ],
                    value="concentric",
                    labelStyle={
                        "display": "inline-block",
                        "margin": "6px",
                    },
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                # html.Button(
                #     id="autogate-button", children="AutoGate"
                # ),
                # html.Label("Center Frequency(ns)"),
                # dcc.Slider(
                #     id="center-slider",
                #     min=-t_max,
                #     max=t_max,
                #     value=0,
                #     step=dt * 10,
                #     marks={
                #         str(int(x)): str(int(x))
                #         for x in np.linspace(-t_max, t_max, 13)
                #     },
                # ),
                # html.Label("Span Frequency(ns)"),
                # dcc.Slider(
                #     id="span-slider",
                #     min=0,
                #     max=t_max,
                #     value=10,
                #     step=dt * 10,
                #     marks={
                #         str(int(x)): str(int(x))
                #         for x in np.linspace(-t_max, t_max, 13)
                #     },
                # ),
            ],
        ),
    ],
)
charts = html.Div(
    [
        cyto.Cytoscape(
            id='cytoscape',
            elements=[],
            layout={'name': 'concentric'},
            style={'width': '100%', 'height': '1000px'},
            stylesheet=[]
        )
        ,
        dcc.Graph(
            id="time-graph", figure={"layout": {"height": 300}}
        ),
        dcc.Graph(
            id="freq-graph", figure={"layout": {"height": 400}}
        ),
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
    Output("cytoscape", "elements"),
    Output("avg_degree", "children"),
    Output("avg_path_len", "children"),
    Output("cluster_co", "children"),
    Input("window-dropdown", "value"),
)
def update_figure(book):
    graph = None
    if book == 'red':
        graph = red_graph
    elif book == 'kingdom':
        graph = kingdom_graph
    elif book == 'west':
        graph = west_graph
    elif book == 'who':
        graph = who_graph
    ss, e = graph_to_view(graph)
    return e, "{:.2f}".format(graph.get_average_degree()), "{:.2f}".format(
        graph.get_average_path_length()), "{:.2f}".format(graph.get_cluster_coefficient()),


@app.callback(
    Output("cytoscape", "stylesheet"),
    Input("window-dropdown", "value"),
)
def update_figure(book):
    global ss
    if book == 'red':
        ss, e = graph_to_view(red_graph)
    elif book == 'kingdom':
        ss, e = graph_to_view(kingdom_graph)
    elif book == 'west':
        ss, e = graph_to_view(west_graph)
    elif book == 'who':
        ss, e = graph_to_view(who_graph)
    return ss


@app.callback(
    Output("cytoscape", "layout"),
    Input("layout-radio", "value")
)
def update_figure(layout):
    layout = {"name": layout}
    return layout
