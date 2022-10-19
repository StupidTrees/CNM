from backend.loader import *


class ViewModel:
    def __init__(self):
        self.keys = ['red', 'west', 'kingdom', 'who']
        self.graphs = {}
        self.graph_raw = {}
        self.current_graph = None
        for key in self.keys:
            if key == 'red':
                self.graph_raw[key] = load_red_graph()
                self.graphs[key] = load_red_graph()
            elif key == 'west':
                self.graph_raw[key] = load_west_graph()
                self.graphs[key] = load_west_graph()
            elif key == 'kingdom':
                self.graph_raw[key] = load_kingdom_graph()
                self.graphs[key] = load_kingdom_graph()
            else:
                self.graph_raw[key] = load_who_graph()
                self.graphs[key] = load_who_graph()
        self.is_ia = False
        self.ia_selected = []

    def get_graph(self, key, reset=False):
        if reset:
            if key == 'red':
                self.graphs[key] = load_red_graph()
            elif key == 'west':
                self.graphs[key] = load_west_graph()
            elif key == 'kingdom':
                self.graphs[key] = load_kingdom_graph()
            else:
                self.graphs[key] = load_who_graph()
            self.current_graph = self.graphs[key]
            return self.graph_raw[key]
        else:
            self.current_graph = self.graphs[key]
            return self.graphs[key]
