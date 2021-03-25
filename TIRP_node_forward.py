
class TIRP_node_forward (object):

    def __init__(self, value=None,children=[]):
        self.value = value
        self.children = children


    def get_value(self):
        return self.value

    def get_children(self):
        return self.children

    def add_child(self,tirp_child):
        self.children.append(tirp_child)

    def get_tirp_by_symbols(self,tirp_symbols):
        if (self.value is None) or (self.value.get_symbols() != tirp_symbols):
            for child in self.children:
                if child.value.get_symbols() == tirp_symbols[0:child.value.get_size()]:
                    return child.get_tirp_by_symbols(tirp_symbols=tirp_symbols)
        else:
            return self



