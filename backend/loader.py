import random
from backend.model.graph import Graph


def generate_random_graph(size):
    g = Graph()
    for i in range(size):
        g.add_node("node{}".format(i),"node{}".format(i))
    rdm = random.Random()
    for i in range(size * (size - 1) // 2):
        if rdm.random() > 0.8:
            rf = [i for i in g.id2nodes.keys()][rdm.randint(0, g.size - 1)]
            rt = [i for i in g.id2nodes.keys()][rdm.randint(0, g.size - 1)]
            while rf == rt:
                rf = [i for i in g.id2nodes.keys()][rdm.randint(0, g.size - 1)]
                rt = [i for i in g.id2nodes.keys()][rdm.randint(0, g.size - 1)]
            g.add_edge(rf, rt, rdm.randint(1, 3))
    return g


def load_red_graph():
    g = Graph()
    with open('backend/data/red/names.txt', 'r') as f:
        for x in f.readlines():
            g.add_node(x.strip(), x.strip())
    with open('backend/data/red/edges_Mandarin.csv', 'r') as f:
        for ed in f.readlines():
            ed = ed.split(";")
            g.add_edge(ed[0].strip(), ed[1].strip(), float(ed[2].strip()))
    return g
