import json


class state_reader (object):

    def __init__(self, states_file):
        self.states_file = states_file
        self.states_json=self.create_states_map()


    def create_states_map(self):
        with open(self.states_file) as f:
            return json.load(f)

    def get_json(self):
        return self.states_json
