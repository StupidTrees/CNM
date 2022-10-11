import random

from backend.model.node import Node


class Graph:

    def __init__(self):
        self.size = 0
        self.nodes = set()
        self.nodes2id = {}
        self.id2nodes = {}
        self.edges = {}
        self.nodes_id_ptr = 0

    def add_node(self, label="", id=None):
        n = Node(self, self.nodes_id_ptr if id is None else id, label)
        self.nodes_id_ptr += 1
        self.nodes2id[n] = n.id
        self.id2nodes[n.id] = n
        self.nodes.add(n)
        self.size += 1

    def add_edge(self, from_id, to_id, weight=0.0):
        if from_id in self.nodes2id.values() and to_id in self.nodes2id.values():
            if from_id not in self.edges.keys():
                self.edges[from_id] = []
            self.edges[from_id].append((to_id, weight))
            self.id2nodes[from_id].neighbours.append((self.id2nodes[to_id], weight))
            self.id2nodes[to_id].prevs.append((self.id2nodes[from_id], weight))


