class Node:
    def __init__(self, graph, id, label=""):
        self.graph = graph
        self.label = label
        self.id = id
        self.neighbours = []
        self.prevs = []

    def get_degree(self):
        return len(self.neighbours) + len(self.prevs)

    def get_degree_in(self):
        return len(self.prevs)

    def get_degree_out(self):
        return len(self.neighbours)
