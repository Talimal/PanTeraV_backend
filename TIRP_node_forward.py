
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

    def get_tirp(self,tirp_symbols,tirp_relations):
        if (self.value is None) or (self.value.get_symbols() != tirp_symbols):
            for child in self.children:
                n=child.value.get_size()
                relations_to_check = []
                if n>1:
                    relations_to_check = tirp_relations[0:int((n*(n-1))/2)]
                if child.value.get_symbols() == tirp_symbols[0:child.value.get_size()] \
                        and child.value.get_relations() == relations_to_check:

                    return child.get_tirp(tirp_symbols=tirp_symbols,tirp_relations=tirp_relations)
        else:
            return self



