import math

import numpy as np

from backend.model.node import Node
from utils.color import random_color


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
        self.coreness = {}
        self.connected_components_num = None

    # 构建图
    def add_node(self, label="", id=None):
        n = Node(self, self.nodes_id_ptr if id is None else id, label)
        self.nodes_id_ptr += 1
        self.nodes2id[n] = n.id
        self.id2nodes[n.id] = n
        self.nodes.add(n)
        self.size += 1

    def remove_nodes(self, node_ids):
        for id in node_ids:
            nn = self.id2nodes[id]
            for nb_id in nn.get_all_neighbour_id():
                nb = self.id2nodes[nb_id]
                nb.remove_neighbour(id)
            if id in self.edges.keys():
                del self.edges[id]
            for fe, tes in self.edges.items():
                if id in tes.keys():
                    del tes[id]
            if nn in self.coreness.keys():
                del self.coreness[nn]
            if nn in self.cluster_coefficient.keys():
                del self.cluster_coefficient[nn]
            self.nodes.remove(nn)

    def add_edge(self, from_id, to_id, weight=0.0):
        if from_id == to_id:
            return
        if from_id in self.nodes2id.values() and to_id in self.nodes2id.values():
            if from_id not in self.edges.keys():
                self.edges[from_id] = {}
            self.edges[from_id][to_id] = weight
            self.id2nodes[from_id].neighbours[to_id] = weight
            self.id2nodes[to_id].prevs[from_id] = weight

    # 基本参数的计算
    def get_average_degree(self):
        res = 0
        for n in self.nodes:
            res += n.get_degree()
        return res / len(self.nodes)

    def get_connected_component_num(self):
        """
        获得连通分量数
        """
        if self.connected_components_num is None:
            self.calc_connected_components_num()
        return self.connected_components_num

    def calc_dists(self):
        """
        计算任意两个节点之间的距离
        """
        dists = {}
        for n in self.nodes:
            u = []
            v = [x.id for x in self.nodes]
            dis = {id: math.inf for id in v}
            dis[n.id] = 0
            while len(v) > 0:
                v = sorted(v, key=lambda x: dis[x])
                fir = self.id2nodes[v.pop(0)]
                u.append(fir.id)
                for nxt_id in fir.get_all_neighbour_id():
                    if nxt_id not in u:
                        dis[nxt_id] = min(dis[nxt_id], dis[fir.id] + 1)
                        u.append(nxt_id)
                    if (fir, n) not in dists.keys():
                        dists[(n, fir)] = dis[fir.id]
        self.dists = dists

    def calc_connected_components_num(self):
        visit = []
        num = 0
        for node in self.nodes:
            if node.id in visit:
                continue
            num += 1
            queue = [node.id]
            while len(queue) > 0:
                x = queue.pop(0)
                for nb_id in self.id2nodes[x].get_all_neighbour_id():
                    if nb_id not in visit:
                        visit.append(nb_id)
                        queue.append(nb_id)
        self.connected_components_num = num

    def calc_cluster_coefficient(self):
        """
        计算每个节点的聚类系数
        """
        for node in self.nodes:
            e = node.get_degree()
            if e == 1 or e == 0:
                self.cluster_coefficient[node] = e
            else:
                r = 0
                visit = []
                neighbours = [n_id for n_id in node.get_all_neighbour_id()]
                for nb_id in neighbours:
                    nb = self.id2nodes[nb_id]
                    for nb_nb_id in nb.get_all_neighbour_id():
                        if nb_nb_id in neighbours:
                            if (nb_id, nb_nb_id) not in visit and (nb_nb_id, nb_id) not in visit:
                                visit.append((nb_id, nb_nb_id))
                                r += 1
                self.cluster_coefficient[node] = r / (e * (e - 1) / 2)

    def calc_coreness(self):
        """
        计算coreness
        """
        degrees = {}
        for node in self.nodes:
            degrees[node] = node.get_degree()
        k = 1
        coreness = {}
        while len(degrees) > 0:
            for node in list(degrees.keys()):
                if node in degrees.keys() and degrees[node] <= k - 1:
                    coreness[node] = k - 1  # 删去时，记录coreness
                    del degrees[node]
                    for nb in node.get_all_neighbour_id():
                        if nb in degrees.keys():
                            degrees[nb] = degrees[nb] - 1
                            if degrees[nb] <= k - 1:
                                del degrees[nb]
                                coreness[nb] = k - 1
            k += 1
        self.coreness = coreness

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

    def get_coreness(self):
        return max(self.coreness.values())

    def get_degree_distribution(self):
        dis = {}
        for node in self.nodes:
            dis.setdefault(node.get_degree(), 0)
            dis[node.get_degree()] += 1
        return dis

    def get_node_class(self, node):
        """
        获得结点类别，例如红楼梦的家族，三国的势力
        :param node:
        :return: string，class
        """
        return node.label[0]

    def get_node_color_map(self):
        class_color_map = {}
        for node in self.nodes:
            node_class = self.get_node_class(node)
            class_color_map[node_class] = random_color(len(class_color_map))
        return class_color_map

    def get_popular_nodes(self, n=None):
        nodes = [(n, n.get_degree()) for n in self.nodes]
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        if n is None:
            n = len(nodes)
        return nodes[:n]

    def get_low_cluster_nodes(self, n=None):
        nodes = [(n, v) for n, v in self.cluster_coefficient.items()]
        nodes = sorted(nodes, key=lambda x: x[1], reverse=False)
        if n is None:
            n = len(nodes)
        return nodes[:n]

    def get_high_coreness_nodes(self, n=None):
        nodes = [(n, cn) for n, cn in self.coreness.items()]
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        if n is None:
            n = len(nodes)
        return nodes[:n]
