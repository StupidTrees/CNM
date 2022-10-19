import os.path

from backend.loader import *
from utils.config import raw_path


class ViewModel:
    def __init__(self):
        name_map = {}
        with open(raw_path + "/name_map", 'r') as f:
            for line in f.readlines():
                name_map[line.split(':')[0].strip()] = line.split(':')[1].strip()
        self.keys = []
        self.names = []
        for file_name in os.listdir(raw_path):
            if not os.path.isdir(raw_path+file_name):
                continue
            self.keys.append(file_name.strip())
            if file_name in name_map.keys():
                self.names.append(name_map[file_name])
            else:
                self.names.append(file_name)
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
            elif key == 'who':
                self.graph_raw[key] = load_who_graph()
                self.graphs[key] = load_who_graph()
            else:
                self.graph_raw[key] = load_any_graph(key)
                self.graphs[key] = load_any_graph(key)

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
            elif key == 'who':
                self.graphs[key] = load_who_graph()
            else:
                self.graphs[key] = load_any_graph(key)
            self.current_graph = self.graphs[key]
            return self.graph_raw[key]
        else:
            self.current_graph = self.graphs[key]
            return self.graphs[key]
