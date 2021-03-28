"""this class is responsible for holding :
        symbol
        relations vector below it
        all the vector symbols after it in the tirps tree"""


class Symbol_Vector_forward(object):

    def __init__(self, symbol=None, relation_vector=[], next_symbol_vectors=[]):
        self.symbol = symbol
        self.relation_vector = relation_vector
        self.next_symbol_vectors = next_symbol_vectors

    def get_symbol(self):
        return self.symbol

    def get_relation_vector(self):
        return self.relation_vector

    def get_next_symbol_vectors(self):
        return self.next_symbol_vectors

    def add_next_symbol_vectors(self, symbol_vector):
        self.next_symbol_vectors.append(symbol_vector)
