from Visualization.Tali import TIRP, TIRP_node_forward, Tirp_node_backwards, Symbol_Vector, Symbol_vector_forward, relations_vector

"""for every line from the KL output file, creates a tirp"""


def get_supporting_instances(entities, instances, line_vector, symbols, index, next_line):
    import re
    import sys
    from Visualization.SymbolicTimeInterval import SymbolicTimeInterval
    from Visualization.SupportingInstance import SupportingInstance

    next_line_parsed = re.split('[ \[ , \]]', next_line)
    line = line_vector[index + 8:]
    for word in range(0, len(line) - 4, 5):
        entity_id = line[word]
        instance_vec = []
        symbolic_list = []
        tis = list(filter(None, line[word + 1].split(']')))
        for t in range(0, len(tis)):
            times = tis[t].split('-')
            start_time = int(times[0].replace("[", ""))
            end_time = int(times[1])
            if start_time == end_time:
                sys.exit("Error! Start time can't be equal to end time! please change KLC code")
            symbolic = SymbolicTimeInterval(start_time=start_time, end_time=end_time, symbol=symbols[
                t])  # , duration=tis[t+1], offset_from_start=tis[t+2], offset_from_end=tis[t+3])
            symbolic_list.append(symbolic)
        instance_vec.append(symbolic_list)
        if entity_id in entities:
            instances[len(instances) - 1].add_list_to_intervals(instance_vec)
        else:
            if len(instances) > 0:
                instances[len(instances) - 1].set_means()
            for i in range(0, len(next_line_parsed) - 9, 11):
                if entity_id == next_line_parsed[i]:
                    mean_duration = float(next_line_parsed[i + 7])
                    mean_offset_from_start = float(next_line_parsed[i + 8])
                    mean_offset_from_end = float(next_line_parsed[i + 9])
                    break
            support_instance = SupportingInstance(entityId=str(entity_id), symbolic_intervals=instance_vec,
                                                  mean_duration=mean_duration,
                                                  mean_offset_from_start=mean_offset_from_start,
                                                  mean_offset_from_end=mean_offset_from_end)
            instances.append(support_instance)
            entities.append(entity_id)
    instance_vec.clear()

class Read_file(object):

    def __init__(self, KLOutput_path):
        """path to the file to read from"""
        self.KLOutput_path = KLOutput_path
        """ there is a difference in KL output due to this parameter"""
        self.calc_offsets = False
        self.calc_offsets = False
        """saving the lines read from the file to later create the TIRPS"""
        self.lines = self.get_lines_from_file(KLOutput_path)
        """CONSTANTS"""
        self.TIRP_SIZE = 0
        self.SYMBOLS = 1
        self.RELATIONS = 2

        self.NUM_SUPPORT_ENTITIES = 3 if not self.calc_offsets else 6
        self.MEAN_HORIZONTAL_SUPPORT = 4 if not self.calc_offsets else 7
        self.OCCURRENCES = 5 if not self.calc_offsets else 8
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

        self.symbols_to_names = {}

    """gets path to KL output and returns all lines"""

    def get_lines_from_file(self, KLOutput_path):
        lines = open(KLOutput_path).read().splitlines()

        import re
        # first line is just karma-lego output parameters
        first_line = lines[0]
        all_params = (re.split(';', first_line))
        params = list(map(lambda param_line: param_line.split('='), all_params))
        # there is a difference in the output of KL due to the 'calc offsets' parameter
        for parameter in params:
            if parameter[0] == 'calc_offsets' and parameter[1] == 'True':
                self.calc_offsets = True

        # actual output lines
        return lines[1:]

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
                        new_symbol_vector = relations_vector.Relations_Vector(symbol=symbol,
                                                                              relation_vector=vector_symbol,
                                                                              prefix_tirps={}, next_tirps={})
                        self.relations_vectors[(symbol, tuple(vector_symbol))] = new_symbol_vector
                    else:
                        new_symbol_vector = self.relations_vectors[(symbol, tuple(vector_symbol))]

                    new_symbol_vector.add_to_prefix_tirps(relations_vector=prev_symbol, tirp=tirp)
                    prev_symbol.add_to_next_tirps(relations_vector=new_symbol_vector, tirp=tirp)
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



    def create_tirps(self):
        tirp_list = []

        lines_size = len(self.lines)
        for line_index in range(0, lines_size, 2):
            first_line = self.lines[line_index]
            first_line_vector = first_line.split(" ")
            second_line = self.lines[line_index + 1]
            second_line_vector = second_line.split(" ")

            line_vector = self.lines[line_index].split()
            next_line = self.lines[line_index + 1]

            instances = []
            entities = list()

            size = int(first_line_vector[self.TIRP_SIZE])
            if size > self.max_tirp_size:
                self.max_tirp_size = size
            # take the symbols only(last place is '' after split)
            symbols = first_line_vector[self.SYMBOLS].split("-")[0:-1]
            # take the relations only(last place is '' after split)
            relations = first_line_vector[self.RELATIONS].split('.')[0:-1]
            num_support_entities = first_line_vector[self.NUM_SUPPORT_ENTITIES]
            mean_horizontal_support = first_line_vector[self.MEAN_HORIZONTAL_SUPPORT]

            # TODO: change this and figure out what it should be?
            occurences = []
            # instances: list = self.get_supporting_instances(line_vector=first_line_vector,
            #                                                 symbols=symbols)
            # entities = self.get_supporting_entities(line_vector=second_line_vector)
            # tirp_obj = Pattern(pattern_size=size,
            #                    symbols=symbols,
            #                    relation=relations,
            #                    supporting_instances=instances,
            #                    supporting_entities=entities,
            #                    mean_horizontal_support=mean_horizontal_support)
            # tirp_list.append(tirp_obj)
            if size > 1:
                index = 0;
            else:
                index = -1;

            mean_duration = float(line_vector[index + 3])
            mean_offset_from_start = float(line_vector[index + 4])
            mean_offset_from_end = float(line_vector[index + 5])
            vertical_support = int(line_vector[index + 6])
            mean_horizontal_support = float(line_vector[index + 7])
            entities = list()
            instances = []
            get_supporting_instances(entities, instances, line_vector, symbols, index=index, next_line=next_line)
            # TIRP_obj = TIRP(tirp_size=TIRP_size, symbols=symbols, relation=relations, supporting_instances=instances,
            #                 supporting_entities=entities, vertical_support=vertical_support,
            #                 mean_horizontal_support=mean_horizontal_support, mean_duration=mean_duration,
            #                 mean_offset_from_start=mean_offset_from_start, mean_offset_from_end=mean_offset_from_end,
            #                 path=path, min_vertical_support=min_ver_support)
            # if class_name == 'class_0':
            #     class_1_tirp = find_tirp_in_class_1(path, TIRP_obj, class_1_tirp_file_name, to_add_entities)
            #     TIRP_obj.set_exist_in_class_0()
            #     if class_1_tirp:
            #         if not to_add_entities:
            #             class_1_tirp = find_tirp_in_class_1(path, TIRP_obj, class_1_tirp_file_name, True)
            #         TIRP_obj.set_class_1_properties(class_1_tirp)
            # if not to_add_entities:
            #     TIRP_obj.set_supporting_instances(list())
            #     TIRP_obj.set_supporting_entitie(list())
            # TIRP_list.append(TIRP_obj)
            new_tirp = TIRP.TIRP(size=size, symbols=symbols, relations=relations,
                                 num_supporting_entities=num_support_entities,
                                 mean_horizontal_support=mean_horizontal_support, occurences=occurences,
                                 supporting_instances=instances,
                                 build_supporting_instances=True
                                 )
            tirp_list.append(new_tirp)
        return tirp_list

    """from the tirps' creates tirps tree with dfs scan - forward regular tirps"""

    def create_tirps_tree(self):
        # dfs scan
        root = TIRP_node_forward.TIRP_node_forward()
        for tirp in self.tirps:
            if tirp.get_size() == 1:
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
                if tirp.get_size() == 1:
                    root.add_child(Tirp_node_backwards.TIRP_node_backwards(value=tirp, children=[]))
                else:
                    n = tirp.get_size() - 1
                    father_symbols = tirp.get_symbols()[1:]
                    father_relations = []
                    if tirp.get_size() > 2:
                        father_relations = tirp.get_relations()[tirp.get_size() - int((n * (n - 1) / 2)):]
                    father = root.get_tirp(father_symbols, father_relations)
                    # TODO: strange that there is a TIRP 2-4-5-7- c.c.<.c.<.<. but not the ending 4-5-7- c.<.<.
                    if father is not None:
                        father.add_child(Tirp_node_backwards.TIRP_node_backwards(value=tirp, children=[]))
                    else:
                        a = 2
        return root

    def set_tirps_names(self,path):
        import json
        with open(path + "\\states.json") as jsonFile:
            for row in jsonFile:
                a = json.loads(row)
                self.symbols_to_names[a['StateID']] = a['TemporalPropertyName'] + '.' + a['BinLabel']
        for tirp in self.tirps:
            symbols_names = []
            for symbol in tirp.get_symbols():
                symbols_names.append(self.symbols_to_names[symbol])
            tirp.set_symbols_names(symbols_names)


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
