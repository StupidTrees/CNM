# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from dash import Dash
from dash.dependencies import Output, Input

from backend.loader import load_red_graph, generate_random_graph
from front.adapter import graph_to_view
from front.view_model import red_graph, kingdom_graph, west_graph, who_graph

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

app = Dash(__name__)

g = load_red_graph()
# app.layout = html.Div([
#     html.H3('红楼梦人物关系图'),
#     graph_to_view(g)
# ])

dt = 1
t_max = 100
######## ## the APP
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
                        html.Div(
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
                                    className="col",
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
                        ),
                        html.Div(
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
                        ),
                    ]
                ),
            ],
        )
    ],
)


@app.callback(
    Output("cytoscape", "elements"),
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
    return e


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


app.run_server(debug=True)
