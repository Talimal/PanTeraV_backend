import TIRP, TIRP_node_forward, Tirp_node_backwards, Symbol_Vector, Symbol_vector_forward, relations_vector


class Read_file(object):

    def __init__(self, KLOutput_path):
        """path to the file to read from"""
        self.KLOutput_path = KLOutput_path
        """saving the lines read from the file to later create the TIRPS"""
        self.lines = self.get_lines_from_file(KLOutput_path)
        """CONSTANTS"""
        self.TIRP_SIZE = 0
        self.SYMBOLS = 1
        self.RELATIONS = 2
        self.NUM_SUPPORT_ENTITIES = 3
        self.MEAN_HORIZONTAL_SUPPORT = 4
        self.OCCURRENCES = 5
        """field to help me later in building the backwards tirps tree in BFS"""
        self.max_tirp_size = 0
        """creating the data structures for later"""
        self.tirps = self.create_tirps()
        self.tirps_tree = self.create_tirps_tree()
        self.tirps_tree_backwrds = self.create_tirps_tree_backwards()
        """structure of symbol_vectors:
         { 
            (symbol:8,relations:[]) : obj:symbol_vector_obj , 
            (symbol:23-65,relations:['<']) : obj:symbol_vector_obj
         
         }"""
        self.symbol_vectors = {}
        self.symbol_vectors_forward = {}
        self.create_symbol_vectors()
        self.create_symbol_vectors_forward()

        self.relations_vectors={}
        self.create_relations_vectors()

    """gets path to KL output and returns all lines"""

    def get_lines_from_file(self, KLOutput_path):
        file = open(KLOutput_path, "r")
        # first line is just karma-lego output parameters
        file.readline()
        # actual output lines
        lines = file.readlines()
        file.close()
        return lines

    """creates a dictionary that each entry is a tuple of symbol and
     it's relations and value is the vectors before it"""

    def create_symbol_vectors(self):
        for tirp in self.tirps:
            prev_symbol = None
            for symbol in tirp.get_symbols():
                index_symbol = tirp.get_symbols().index(symbol)
                if index_symbol == 0:
                    if (symbol, tuple([])) not in self.symbol_vectors:
                        prev_symbol = Symbol_Vector.Symbol_Vector(symbol=symbol, relation_vector=[],
                                                                  previous_symbol_vectors=[])
                        self.symbol_vectors[(symbol, tuple([]))] = prev_symbol
                    else:
                        prev_symbol = self.symbol_vectors[(symbol, tuple([]))]
                else:
                    vector_symbol = []
                    sum_relations_till_now = 0

                    for index in range(0, index_symbol):
                        vector_symbol.append(tirp.get_relations()[sum_relations_till_now + index_symbol - index - 1])
                        sum_relations_till_now += index_symbol - index

                    if (symbol, tuple(vector_symbol)) not in self.symbol_vectors:
                        new_symbol_vector = Symbol_Vector.Symbol_Vector(symbol=symbol, relation_vector=vector_symbol,
                                                                        previous_symbol_vectors=[])
                        self.symbol_vectors[(symbol, tuple(vector_symbol))] = new_symbol_vector
                    else:
                        new_symbol_vector = self.symbol_vectors[(symbol, tuple(vector_symbol))]

                    new_symbol_vector.add_previous_symbol_vector(prev_symbol)
                    prev_symbol = new_symbol_vector

    def create_relations_vectors(self):
        for tirp in self.tirps:
            prev_symbol = None
            for symbol in tirp.get_symbols():
                index_symbol = tirp.get_symbols().index(symbol)
                if index_symbol == 0:
                    if (symbol, tuple([])) not in self.relations_vectors:
                        prev_symbol = relations_vector.Relations_Vector(symbol=symbol, relation_vector=[],
                                                                  prefix_tirps={}, next_tirps={})
                        self.relations_vectors[(symbol, tuple([]))] = prev_symbol
                    else:
                        prev_symbol = self.relations_vectors[(symbol, tuple([]))]
                else:
                    vector_symbol = tirp.get_vector_in_size(index_symbol)

                    if (symbol, tuple(vector_symbol)) not in self.relations_vectors:
                        new_symbol_vector = relations_vector.Relations_Vector(symbol=symbol, relation_vector=vector_symbol,
                                                                        prefix_tirps={}, next_tirps={})
                        self.relations_vectors[(symbol, tuple(vector_symbol))] = new_symbol_vector
                    else:
                        new_symbol_vector = self.relations_vectors[(symbol, tuple(vector_symbol))]

                    new_symbol_vector.add_to_prefix_tirps(relations_vector=prev_symbol,tirp=tirp)
                    prev_symbol.add_to_next_tirps(relations_vector=new_symbol_vector,tirp=tirp)
                    prev_symbol = new_symbol_vector


    """creates a dictionary that each entry is a tuple of symbol and
     it's relations and value is the vectors after it"""

    def create_symbol_vectors_forward(self):
        for tirp in self.tirps:
            prev_symbol = None
            for symbol in tirp.get_symbols():
                index_symbol = tirp.get_symbols().index(symbol)
                if index_symbol == 0:
                    if (symbol, tuple([])) not in self.symbol_vectors_forward:
                        prev_symbol = Symbol_vector_forward.Symbol_Vector_forward(symbol=symbol, relation_vector=[],
                                                                                  next_symbol_vectors=[])
                        self.symbol_vectors_forward[(symbol, tuple([]))] = prev_symbol
                    else:
                        prev_symbol = self.symbol_vectors_forward[(symbol, tuple([]))]
                else:
                    vector_symbol = []
                    sum_relations_till_now = 0

                    for index in range(0, index_symbol):
                        vector_symbol.append(tirp.get_relations()[sum_relations_till_now + index_symbol - index - 1])
                        sum_relations_till_now += index_symbol - index

                    if (symbol, tuple(vector_symbol)) not in self.symbol_vectors_forward:
                        new_symbol_vector = Symbol_vector_forward.Symbol_Vector_forward(symbol=symbol,
                                                                                        relation_vector=vector_symbol,
                                                                                        next_symbol_vectors=[])
                        self.symbol_vectors_forward[(symbol, tuple(vector_symbol))] = new_symbol_vector
                    else:
                        new_symbol_vector = self.symbol_vectors_forward[(symbol, tuple(vector_symbol))]

                    prev_symbol.add_next_symbol_vectors(new_symbol_vector)
                    prev_symbol = new_symbol_vector

    """for every line from the KL output file, creates a tirp"""

    def create_tirps(self):
        tirps = []
        for line in self.lines:
            line_components = line.split(" ")
            size = int(line_components[self.TIRP_SIZE])
            # take the symbols only(last place is '' after split)
            symbols = line_components[self.SYMBOLS].split("-")[0:-1]
            # take the relations only(last place is '' after split)
            relations = line_components[self.RELATIONS].split('.')[0:-1]
            num_support_entities = line_components[self.NUM_SUPPORT_ENTITIES]
            mean_horizontal_support = line_components[self.MEAN_HORIZONTAL_SUPPORT]
            occurrences = line_components[self.OCCURRENCES:]
            new_tirp = TIRP.TIRP(size=size, symbols=symbols, relations=relations,
                                 num_supporting_entities=num_support_entities,
                                 mean_horizontal_support=mean_horizontal_support, occurences=occurrences)
            tirps.append(new_tirp)

            if size > self.max_tirp_size:
                self.max_tirp_size = size

        return tirps

    """from the tirps' creates tirps tree with dfs scan - forward regular tirps"""

    def create_tirps_tree(self):
        # dfs scan
        root = TIRP_node_forward.TIRP_node_forward()
        for tirp in self.tirps:
            if tirp.size == 1:
                root.add_child(TIRP_node_forward.TIRP_node_forward(value=tirp, children=[]))
            else:
                n = tirp.get_size() - 1
                father_symbols = tirp.get_symbols()[:-1]
                father_relations = []
                if tirp.get_size() > 2:
                    father_relations = tirp.get_relations()[0:int((n * (n - 1)) / 2)]

                father = root.get_tirp(father_symbols, father_relations)
                father.add_child(TIRP_node_forward.TIRP_node_forward(value=tirp, children=[]))
        return root

    """gets a desired size and returns all tirps in that size"""

    def get_tirps_in_size(self, size):
        result = []
        for tirp in self.tirps:
            if tirp.get_size() == size:
                result.append(tirp)
        return result

    """from the tirps' creates tirps tree with bfs scan - backwards mining"""

    def create_tirps_tree_backwards(self):
        # bfs scan
        root = Tirp_node_backwards.TIRP_node_backwards()
        for index in range(1, self.max_tirp_size + 1):
            for tirp in self.get_tirps_in_size(index):
                if tirp.size == 1:
                    root.add_child(Tirp_node_backwards.TIRP_node_backwards(value=tirp, children=[]))
                else:
                    n = tirp.get_size() - 1
                    father_symbols = tirp.get_symbols()[1:]
                    father_relations = []
                    if tirp.get_size() > 2:
                        father_relations = tirp.get_relations()[tirp.get_size() - int((n * (n - 1) / 2)):]
                    father = root.get_tirp(father_symbols, father_relations)
                    father.add_child(Tirp_node_backwards.TIRP_node_backwards(value=tirp, children=[]))

        return root

    """returns all tirps"""

    def get_tirps(self):
        return self.tirps

    """returns forward tree"""

    def get_forward_tree(self):
        return self.tirps_tree

    """returns backwards tree"""

    def get_backwards_tree(self):
        return self.tirps_tree_backwrds

    def get_relations_vectors(self):
        return self.relations_vectors
