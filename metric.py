import json
import uuid
import os
import time

class Metric:
    def __init__(self) -> None:
        self.count = 0
        self.nodes_file = None
        self.results_file = None
        self.nodes = []
        self.results = {"minimax": {}, "alphabeta": {}}
        self.last_movement = None
        self.avg_time = 0
        self.start_time = None
        self.end_time = None
    
    def get_alg_name(self, algorithm_num):
        if algorithm_num == 0:
            return "minimax"
        
        return "alphabeta"

    def open_nodes_file(self, algorithm):
        filename = './out/'+ self.get_alg_name(algorithm) +'/nodes.json'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return open(filename, 'w')
    
    def open_results_file(self):
        filename = './out/results.json'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return open(filename, 'w')

    def init_tree(self, algorithm):
        self.nodes = []
        self.last_movement = None
        self.count = 0
        
    def save_tree(self, algorithm):
        nodes_file = self.open_nodes_file(algorithm)
        results_file = self.open_results_file()

        self.results[self.get_alg_name(algorithm)] = {
            "nodes": len(self.nodes),
            "avgTime": self.avg_time / self.count,
        }
        
        print(json.dumps(self.results), self.results_file, self.nodes_file)
        results_file.write(json.dumps(self.results))
        nodes_file.write(json.dumps(self.nodes))


    def add_movement(self, name, state):
        id = uuid.uuid4()
        self.last_movement = id
        self.nodes.append({"type": "MOVEMENT", "name": name, "id": str(id), "state": self.get_output_state(state)})
        return id
    
    def add_parent(self, name, state):
        id = uuid.uuid4()
        self.nodes.append({"type": "PARENT", "name": name, "id": str(id), "parent": str(self.last_movement), "state": self.get_output_state(state)})
        return id
    
    def add_action(self, parent, state):
        id = uuid.uuid4()
        self.nodes.append({"type": "ACTION", "id": str(id), "parent": str(parent), "state": self.get_output_state(state)})
        return id
    
    def get_output_state(self, state):
        res = ""
        for i in range(len(state)):
            res += ' {} | {} | {}'.format(*state[i])
            if i < len(state) - 1:
                res += '\n--+--+--\n'

        return res
    
    def start_duration(self):
        self.count += 1
        self.start_time = time.time()
    
    def end_duration(self):
        self.avg_time += time.time() - self.start_time
    