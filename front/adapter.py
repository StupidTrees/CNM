import random

import dash_cytoscape as cyto

from utils.color import random_color


def graph_to_view(graph, degree_range=None):
    if degree_range is None:
        degree_range = [0, 1000]
    elements = []
    class_color_map = {}
    for node in graph.nodes:
        node_class = graph.get_node_class(node)
        if degree_range[1] >= node.get_degree() >= degree_range[0]:
            class_color_map[node_class] = random_color(len(class_color_map))
            elements.append(
                {"data": {"id": str(node.id), "label": node.label, 'class_name': graph.get_node_class(node)}, })
    for fe, tes in graph.edges.items():
        for te, weight in tes:
            fen = graph.id2nodes[fe]
            ten = graph.id2nodes[te]
            if degree_range[1] < fen.get_degree() or fen.get_degree() < degree_range[0] or degree_range[
                1] < ten.get_degree() or ten.get_degree() < degree_range[0]:
                continue
            dom = fen if fen.get_degree() > ten.get_degree() else ten
            elements.append({"data": {"source": str(fe), "target": str(te), "weight": weight,
                                      "dom_class_name": graph.get_node_class(dom)}})
    ss = [
        {'selector': 'node',
         'style': {
             'label': 'data(label)'
         }},
        {'selector': 'edge',
         'style': {
             "curve-style": "bezier",
             'width': "2px",
             'line-opacity': "50%"
         }}]
    for fn, cl in class_color_map.items():
        ss.append(
            {'selector': '[class_name *= "{}"]'.format(fn),
             'style': {
                 'background-color': '{}'.format(cl)
             }}
        )
        ss.append({'selector': '[dom_class_name *= "{}"]'.format(fn),
                   'style': {
                       'line-color': '{}'.format(cl),
                   }})
    return ss, elements
