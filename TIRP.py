
class TIRP (object):

    def __init__(self, size, symbols, relations, num_supporting_entities, mean_horizontal_support, occurences):
        self.size = size
        self.symbols = symbols
        self.relations = relations
        self.num_supporting_entities = num_supporting_entities
        self.mean_horizontal_support = mean_horizontal_support
        self.occurences = occurences

    def get_symbols(self):
        return self.symbols

    def get_size(self):
        return self.size

    def get_relations(self):
        return self.relations

    def get_mean_horizontal_support(self):
        return self.mean_horizontal_support

    """gets a list and returns a string (like toString())"""
    def convert_list_to_string(self,list):
        str=""
        for item in list:
            str=str+" "+item
        return str

    """gets a list of symbols and returns a string (like toString())"""
    def string_symbols(self,symbols):
        str = symbols[0]
        for i in range(1,len(symbols),1):
            str = str+"-"+symbols[i]
        return str

    """gets a list of relations and returns a string (like toString())"""
    def string_relations(self,relations):
        if len(relations)>0:
            str = relations[0]+"."
            for i in range(1,len(relations),1):
                str = str+relations[i]+"."
            return str
        else:
            return ""

    def __str__(self):
        a=self.convert_list_to_string(self.occurences)
        return "("+str(self.size)+", "+self.string_symbols(self.symbols)+", "+\
               self.string_relations(self.relations)+", "+self.num_supporting_entities+", "+self.mean_horizontal_support+", "+\
               self.convert_list_to_string(self.occurences)+")"