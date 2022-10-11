import dash_cytoscape as cyto

from utils.color import random_color


def graph_to_view(graph):
    elements = []
    family_color_map = {}
    for node in graph.nodes:
        family_name = node.label[0]
        family_color_map[family_name] = random_color(len(family_color_map))
        elements.append({"data": {"id": str(node.id), "label": node.label, 'family_name': node.label[0]}, })
    for fe, tes in graph.edges.items():
        for te, weight in tes:
            dom = fe if graph.id2nodes[fe].get_degree() > graph.id2nodes[te].get_degree() else te
            elements.append({"data": {"source": str(fe), "target": str(te), "weight": weight, "dom_family": dom[0]}})
    ss = [
        {'selector': 'node',
         'style': {
             'label': 'data(label)'
         }},
        {
            'selector': '.high',
            'style': {
                'background-color': 'red',
                'line-color': 'red'
            }
        }]
    for fn, cl in family_color_map.items():
        ss.append(
            {'selector': '[family_name *= "{}"]'.format(fn),
             'style': {
                 'background-color': '{}'.format(cl)
             }}
        )
        ss.append({'selector': '[dom_family *= "{}"]'.format(fn),
                   'style': {
                       'line-color': '{}'.format(cl),
                       'line-width':"0.1px"
                   }})
    return ss,elements
