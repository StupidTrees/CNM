import os.path
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


def load_graph(clz, label):
    sys.setrecursionlimit(3000)
    g = clz()
    if path.exists("backend/model/cache/{}.pkl".format(label)):
        print('load graph {} from disk...'.format(label))
        return pickle.load(open("backend/model/cache/{}.pkl".format(label), 'rb'))
    with open('backend/data/parsed/{}/names.txt'.format(label), 'r') as f:
        for x in f.readlines():
            g.add_node(x.strip(), x.strip())
    with open('backend/data/parsed/{}/edges.txt'.format(label), 'r') as f:
        for ed in f.readlines():
            ed = ed.split(";")
            n1 = ed[0].strip()
            n2 = ed[1].strip()
            g.add_edge(n1, n2, float(ed[2].strip()))
    print('calculating properties for graph {}'.format(label))
    g.calc_dists()
    g.calc_coreness()
    g.calc_cluster_coefficient()
    print('calculation properties for graph {} done'.format(label))
    if not os.path.exists("backend/model/cache/"):
        os.makedirs("backend/model/cache/")
    pickle.dump(g, open("backend/model/cache/{}.pkl".format(label), "wb"))
    return g


class RedGraph(Graph):
    def get_node_class(self, node):
        return node.label[0]


class KingdomGraph(Graph):
    def __init__(self):
        super().__init__()
        self.country_map = {}
        with open('backend/data/parsed/kingdom/countries/qun.txt', 'r') as f:
            for name in f.readlines():
                self.country_map[name.strip()] = 'qun'
        with open('backend/data/parsed/kingdom/countries/wei.txt', 'r') as f:
            for name in f.readlines():
                self.country_map[name.strip()] = 'wei'
        with open('backend/data/parsed/kingdom/countries/shu.txt', 'r') as f:
            for name in f.readlines():
                self.country_map[name.strip()] = 'shu'
        with open('backend/data/parsed/kingdom/countries/wu.txt', 'r') as f:
            for name in f.readlines():
                self.country_map[name.strip()] = 'wu'

    def get_node_color_map(self):
        return {
            'wei': "#097AFF",
            "shu": "#FD9A28",
            "wu": "#3abc98",
            "qun": "#C1CBCA"
        }

    def get_node_class(self, node):
        if node.label in self.country_map.keys():
            return self.country_map[node.label]
        else:
            return 'qun'


class WestGraph(Graph):
    def get_node_class(self, node):
        return node.label[0]


class WhoGraph(Graph):
    def get_node_class(self, node):
        return node.label[0]


def load_kingdom_graph():
    return load_graph(KingdomGraph, "kingdom")


def load_red_graph():
    return load_graph(RedGraph, "red")


def load_west_graph():
    return load_graph(RedGraph, "west")


def load_who_graph() -> object:
    return load_graph(WhoGraph, "who")
