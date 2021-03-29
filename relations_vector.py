"""this class is responsible for holding :
        """


class Relations_Vector(object):

    def __init__(self, symbol=None, relation_vector=[], prefix_tirps={},next_tirps={}):
        self.symbol = symbol
        self.relation_vector = relation_vector
        self.prefix_tirps = prefix_tirps
        self.next_tirps = next_tirps


    def get_symbol(self):
        return self.symbol

    def get_relation_vector(self):
        return self.relation_vector

    def get_prefix_tirps(self):
        return self.prefix_tirps

    def get_next_tirps(self):
        return self.next_tirps

    def add_to_prefix_tirps(self,relations_vector,tirp):
        if (relations_vector.get_symbol(),tuple(relations_vector.get_relation_vector())) not in self.prefix_tirps:
            self.prefix_tirps[(relations_vector.get_symbol(),tuple(relations_vector.get_relation_vector()))]=[tirp]
        else:
            self.prefix_tirps[(relations_vector.get_symbol(),tuple(relations_vector.get_relation_vector()))].append(tirp)

    def add_to_next_tirps(self,relations_vector,tirp):
        if (relations_vector.get_symbol(), tuple(relations_vector.get_relation_vector())) not in self.next_tirps:
            self.next_tirps[(relations_vector.get_symbol(), tuple(relations_vector.get_relation_vector()))] = [tirp]
        else:
            self.next_tirps[(relations_vector.get_symbol(), tuple(relations_vector.get_relation_vector()))].append(
                tirp)

    def get_json_from_field(self,json_tuples):
        result = {}
        for entry in json_tuples:
            result[str(entry[0])+","+self.get_string_from_array(entry[1])] = list(map(lambda tirp: tirp.__dict__, json_tuples[entry]))
        return result

    def get_string_from_array(self,array):
        final_string = ""
        for element in array:
            final_string = final_string + str(element) + ","
        return final_string[:-1]

    def serialize(self):
        return {
            'symbol':self.symbol,
            'relations':self.relation_vector,
            'prefix': self.get_json_from_field(self.prefix_tirps),
            'next': self.get_json_from_field(self.next_tirps),
        }
