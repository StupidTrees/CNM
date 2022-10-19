class Node:
    def __init__(self, graph, id, label=""):
        self.graph = graph
        self.label = label
        self.id = id
        self.neighbours = {}
        self.prevs = {}

    def get_all_neighbour_id(self):
        return list(self.neighbours.keys()) + list(self.prevs.keys())

    def remove_neighbour(self, nb_id):
        if nb_id in self.neighbours.keys():
            del self.neighbours[nb_id]
        if nb_id in self.prevs.keys():
            del self.prevs[nb_id]

    def get_degree(self):
        return len(self.neighbours) + len(self.prevs)

    def get_degree_in(self):
        return len(self.prevs)

    def get_degree_out(self):
        return len(self.neighbours)
