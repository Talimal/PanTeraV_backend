import json
from TIRP_node_forward import TIRP_node_forward
from types import SimpleNamespace

class Create_Forward_Index (object):

    def __init__(self, forward_tree, forward_index_path):
        # output index file path
        self.index_file = open(forward_index_path, "w")

        self.forward_tree = forward_tree

        # creating the index output file
        # self.write_to_index_file(self.forward_tree)
        self.forward_index_path = forward_index_path
        self.serialize_forward_tree(self.forward_tree)
        self.index_file.close()

        self.deserialize_forward_tree()

    """write to the output index file"""
    def write_to_index_file(self,tree_node):
        if tree_node.get_value() == None:
            self.index_file.write("tirp = root"+"\n")
        else:
            self.index_file.write("tirp = " +str(tree_node.get_value())+"\n")

        self.index_file.write("children = [ ")
        for child in tree_node.get_children():
            self.write_to_index_file(child)
        self.index_file.write(" ]")

        self.index_file.write("\n")
        self.index_file.write("--------------------------------------------------------------------------------")
        self.index_file.write("\n")
        self.index_file.write("\n")

    def serialize_forward_tree(self,tree_node):
        json_data = json.dumps(tree_node, default=lambda o: o.__dict__, indent=4)
        self.index_file.write(json_data)

    def deserialize_forward_tree(self):
        # decoded_team = TIRP_node_forward(**json.loads(json_data))

        with open(self.forward_index_path, "r") as my_file_read:
            my_second_list = json.dumps(json.load(my_file_read))
            my_second_list = TIRP_node_forward(**json.loads(my_second_list))
            print(my_second_list)


    """writes the list of tirps to the index output file"""
    def write_to_index_file_tirps(self,tirps):
        for tirp in tirps:
            self.index_file.write(str(tirp))
