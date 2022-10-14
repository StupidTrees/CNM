import pickle
import random
import sys
from os import path

from backend.model.graph import Graph


def generate_random_graph(size):
    g = Graph()
    for i in range(size):
        g.add_node("node{}".format(i), "node{}".format(i))
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


class RedGraph(Graph):
    def get_node_class(self, node):
        return node.label[0]


def load_red_graph():
    g = RedGraph()
    if path.exists("backend/model/red.pkl"):
        return pickle.load(open("backend/model/red.pkl", 'rb'))
    with open('backend/data/red/names.txt', 'r') as f:
        for x in f.readlines():
            g.add_node(x.strip(), x.strip())
    with open('backend/data/red/edges_Mandarin.csv', 'r') as f:
        for ed in f.readlines():
            ed = ed.split(";")
            g.add_edge(ed[0].strip(), ed[1].strip(), float(ed[2].strip()))
    g.calc_dists()
    g.calc_cluster_coefficient()
    pickle.dump(g, open("backend/model/red.pkl", "wb"))
    return g


class KingdomGraph(Graph):
    def get_node_class(self, node):
        return node.label[0]

def load_kingdom_graph():
    sys.setrecursionlimit(3000)
    g = KingdomGraph()
    if path.exists("backend/model/kingdom.pkl"):
        print('load graph from disk...')
        return pickle.load(open("backend/model/kingdom.pkl", 'rb'))
    with open('backend/data/kingdom/names.txt', 'r') as f:
        for x in f.readlines():
            g.add_node(x.strip(), x.strip())
    with open('backend/data/kingdom/edges.txt', 'r') as f:
        for ed in f.readlines():
            ed = ed.split(";")
            n1 = ed[0].strip()
            n2 = ed[1].strip()
            g.add_edge(n1, n2, float(ed[2].strip()))
    print('calculating...')
    g.calc_dists()
    g.calc_cluster_coefficient()
    pickle.dump(g, open("backend/model/kingdom.pkl", "wb"))
    return g
