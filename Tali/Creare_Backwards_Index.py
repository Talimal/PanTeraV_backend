import json
from Visualization.Tali.Tirp_node_backwards import TIRP_node_backwards

class Create_Backwards_Index (object):

    def __init__(self, backwards_tree,backwards_index_path):
        # output index file path
        self.index_file = open(backwards_index_path, "w")
        self.backwards_index_path = backwards_index_path
        self.backwards_tree = backwards_tree

        # creating the index output file
        # self.write_to_index_file(self.backwards_tree)

        self.serialize_backwards_tree(self.backwards_tree)
        self.index_file.close()
        self.deserialize_backwards_tree()

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

    def serialize_backwards_tree(self,tree_node):
        json_data = tree_node.serialize()
        json.dump(json_data, self.index_file)

        # json_data = json.dumps(tree_node, default=lambda o: o.__dict__, indent=4)
        # self.index_file.write(json_data)

    def deserialize_backwards_tree(self):
        # decoded_team = TIRP_node_forward(**json.loads(json_data))

        with open(self.backwards_index_path, "r") as my_file_read:
            my_second_list = json.dumps(json.load(my_file_read))
            my_second_list = TIRP_node_backwards(**json.loads(my_second_list))
            print(my_second_list)

    """writes the list of tirps to the index output file"""
    def write_to_index_file_tirps(self,tirps):
        for tirp in tirps:
            self.index_file.write(str(tirp))
