"""this class is responsible for holding :
        symbol
        relations vector below it
        all the vector symbols before it in the tirps tree"""


class Symbol_Vector(object):

    def __init__(self, symbol=None, relation_vector=[], previous_symbol_vectors=[]):
        self.symbol = symbol
        self.relation_vector = relation_vector
        self.previous_symbol_vectors = previous_symbol_vectors

    def get_symbol(self):
        return self.symbol

    def get_relation_vector(self):
        return self.relation_vector

    def get_previous_symbol_vectors(self):
        return self.previous_symbol_vectors

    def add_previous_symbol_vector(self, symbol_vector):
        self.previous_symbol_vectors.append(symbol_vector)
