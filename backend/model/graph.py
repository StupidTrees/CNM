import math

import numpy as np

from backend.model.node import Node


class Graph:

    def __init__(self):
        self.size = 0
        self.nodes = set()
        self.nodes2id = {}
        self.id2nodes = {}
        self.edges = {}
        self.nodes_id_ptr = 0
        self.dists = {}
        self.cluster_coefficient = {}

    # 构建图
    def add_node(self, label="", id=None):
        n = Node(self, self.nodes_id_ptr if id is None else id, label)
        self.nodes_id_ptr += 1
        self.nodes2id[n] = n.id
        self.id2nodes[n.id] = n
        self.nodes.add(n)
        self.size += 1

    def add_edge(self, from_id, to_id, weight=0.0):
        if from_id == to_id:
            return
        if from_id in self.nodes2id.values() and to_id in self.nodes2id.values():
            if from_id not in self.edges.keys():
                self.edges[from_id] = []
            self.edges[from_id].append((to_id, weight))
            self.id2nodes[from_id].neighbours.append((self.id2nodes[to_id], weight))
            self.id2nodes[to_id].prevs.append((self.id2nodes[from_id], weight))

    # 基本参数的计算
    def get_average_degree(self):
        res = 0
        for n in self.nodes:
            res += n.get_degree()
        return res / len(self.nodes)

    def calc_dists(self):
        dists = {}
        for n in self.nodes:
            u = []
            v = [x for x in self.nodes]
            dis = {x: math.inf for x in v}
            dis[n] = 0
            while len(v) > 0:
                v = sorted(v, key=lambda x: dis[x])
                fir = v.pop(0)
                u.append(fir)
                for nxt, _ in fir.neighbours + fir.prevs:
                    if nxt not in u:
                        dis[nxt] = min(dis[nxt], dis[fir] + 1)
                    if (fir, n) not in dists.keys():
                        dists[(n, fir)] = dis[fir]
        self.dists = dists

    def calc_cluster_coefficient(self):
        for node in self.nodes:
            e = len(node.neighbours) + len(node.prevs)
            if e == 1 or e == 0:
                self.cluster_coefficient[node] = e
            else:
                r = 0
                visit = []
                neighbours = [n for n, _ in node.neighbours + node.prevs]
                for nb in neighbours:
                    for nbn, _ in nb.neighbours + nb.prevs:
                        if nbn in neighbours:
                            if (nb, nbn) not in visit and (nbn, nb) not in visit:
                                visit.append((nb, nbn))
                                r += 1
                self.cluster_coefficient[node] = r / (e * (e - 1) / 2)

    def get_dist(self, x, y):
        if len(self.dists) == 0:
            self.calc_dists()
        xn = self.id2nodes[x]
        yn = self.id2nodes[y]
        if (xn, yn) in self.dists.keys():
            return self.dists[(xn, yn)]
        if (yn, xn) in self.dists.keys():
            return self.dists[(yn, xn)]
        return 0

    def get_average_path_length(self):
        if len(self.dists) == 0:
            self.calc_dists()
        avg = 0
        for x, y in self.dists.items():
            if y != math.inf:
                avg += y
        return avg / len(self.dists)

    def get_cluster_coefficient(self):
        if len(self.cluster_coefficient) == 0:
            self.calc_cluster_coefficient()
        return np.average([x for x in self.cluster_coefficient.values()])

    # 其他功能

    def get_node_class(self, node):
        """
        获得结点类别，例如红楼梦的家族，三国的势力
        :param node:
        :return: string，class
        """
        pass

    def get_popular_nodes(self, n=10):
        nodes = [(n, n.get_degree()) for n in self.nodes]
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        return nodes[:n]

    def get_high_cluster_nodes(self, n=10):
        nodes = [(n, self.cluster_coefficient[n]) for n in self.nodes]
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        return nodes[:n]