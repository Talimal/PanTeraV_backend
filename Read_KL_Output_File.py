import TIRP, TIRP_node_forward, Tirp_node_backwards, Symbol_Vector, Symbol_vector_forward, relations_vector
from Guys_server.pattern import Pattern
from Guys_server.symbolic_time_interval import SymbolicTimeInterval
from Guys_server.entity_tirp_instance import EntityTIRPInstance
from Guys_server.entity_tirp import EntityTIRP


locations = {
    'loc_tirp_size': 0,
    'loc_symbols': 1,
    'loc_relations': 2,
    'loc_mean_mean_duration': 3,
    'loc_mean_start_offset': 4,
    'loc_mean_end_offset': 5,
    'loc_vertical_support': 6,
    'loc_mean_horizontal_support': 7,
    'loc_start_entities': 8
}

class Read_file(object):

    def __init__(self, KLOutput_path):
        """path to the file to read from"""
        self.KLOutput_path = KLOutput_path
        """ there is a difference in KL output due to this parameter"""
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

    """gets path to KL output and returns all lines"""

    def get_lines_from_file(self, KLOutput_path):

        lines = open(KLOutput_path).read().splitlines()

        import re
        # first line is just karma-lego output parameters
        first_line = lines[0]
        all_params = (re.split(';', first_line))
        params = list(map(lambda param_line: param_line.split('='),all_params))
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

    def get_supporting_instances(self,line_vector, symbols) -> list:
        entity_instances = []
        steps_each_iteration = 5
        for instance_index in range(locations['loc_start_entities'], len(line_vector) - 1, steps_each_iteration):
            start_entity_index = instance_index
            entity_id = int(line_vector[instance_index])
            start_entity_index += 1
            instance_vec = []
            start_time_index, end_time_index = 0, 1
            time_intervals = list(filter(None, line_vector[start_entity_index].split(']')))
            for interval_index in range(0, len(time_intervals)):
                interval: str = time_intervals[interval_index].split('-')
                start_time = int(interval[start_time_index].replace("[", ""))
                end_time = int(interval[end_time_index])
                if start_time == end_time:
                    raise Exception("Error! Start time can\'t be equal to end time!")
                instance_vec.append(SymbolicTimeInterval(start_time=start_time,
                                                         end_time=end_time,
                                                         symbol=symbols[interval_index]))
            start_entity_index += 1
            duration = line_vector[start_entity_index]
            start_entity_index += 1
            offset_from_start = line_vector[start_entity_index]
            start_entity_index += 1
            offset_from_end = line_vector[start_entity_index]
            entity_instances.append(EntityTIRPInstance(instance_vec=instance_vec,
                                                       entity_id=entity_id,
                                                       duration=duration,
                                                       offset_from_start=offset_from_start,
                                                       offset_from_end=offset_from_end))
        return entity_instances

    def get_supporting_entities(self,line_vector):
        entities_list = {}
        steps_each_iteration = 6
        for instance_index in range(0, len(line_vector) - 1, steps_each_iteration):
            start_entity_index = instance_index
            entity_id = int(line_vector[start_entity_index].replace(",", ""))
            start_entity_index += 1
            start_period = int(line_vector[start_entity_index].replace(",", "").replace("[", ""))
            start_entity_index += 1
            end_period = int(line_vector[start_entity_index].replace("]", "").replace(":", ""))
            start_entity_index += 1
            mean_durations = float(line_vector[start_entity_index].replace("]", ""))
            start_entity_index += 1
            offset_from_start = float(line_vector[start_entity_index].replace("]", ""))
            start_entity_index += 1
            offset_from_end = float(line_vector[start_entity_index].replace(",", ""))
            entities_list[entity_id] = EntityTIRP(entity_id=entity_id,
                                                  start_period=start_period,
                                                  end_period=end_period,
                                                  duration=mean_durations,
                                                  offset_from_start=offset_from_start,
                                                  offset_from_end=offset_from_end)
        return entities_list

    def create_tirps_guy(self):
        tirp_list = []
        # lines = [line.rstrip('\n') for line in open(file_path)]
        lines_size = len(self.lines)
        for line_index in range(0, lines_size, 2):
            first_line = self.lines[line_index]
            first_line_vector = first_line.split()
            second_line = self.lines[line_index + 1]
            second_line_vector = second_line.split()
            tirp_size = int(first_line_vector[self.TIRP_SIZE])
            symbols = first_line_vector[self.SYMBOLS].split("-")[0:-1]
            relations = first_line_vector[self.RELATIONS].split('.')[0:-1]
            num_support_entities = first_line_vector[self.NUM_SUPPORT_ENTITIES]
            mean_horizontal_support = first_line_vector[self.MEAN_HORIZONTAL_SUPPORT]



            instances: list = self.get_supporting_instances(line_vector=first_line_vector,
                                                       symbols=symbols)
            entities = self.get_supporting_entities(line_vector=second_line_vector)
            tirp_obj = Pattern(pattern_size=tirp_size,
                               symbols=symbols,
                               relation=relations,
                               supporting_instances=instances,
                               supporting_entities=entities,
                               mean_horizontal_support=mean_horizontal_support)
            tirp_list.append(tirp_obj)
        return tirp_list

    """for every line from the KL output file, creates a tirp"""

    def create_tirps(self):


        tirp_list = []

        lines_size = len(self.lines)
        for line_index in range(0, lines_size, 2):
            first_line = self.lines[line_index]
            first_line_vector = first_line.split(" ")
            second_line = self.lines[line_index + 1]
            second_line_vector = second_line.split(" ")

            size = int(first_line_vector[self.TIRP_SIZE])
            if size>self.max_tirp_size:
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

            new_tirp = TIRP.TIRP(size=size,symbols=symbols,relations=relations,num_supporting_entities=num_support_entities,mean_horizontal_support=mean_horizontal_support,occurences=occurences)
            tirp_list.append(new_tirp)
        return tirp_list

        #     occurrences = line_components[self.OCCURRENCES:]
        #     new_tirp = TIRP.TIRP(size=size, symbols=symbols, relations=relations,
        #                          num_supporting_entities=num_support_entities,
        #                          mean_horizontal_support=mean_horizontal_support, occurences=occurrences)
        #     tirps.append(new_tirp)
        #     if size > self.max_tirp_size:
        #         self.max_tirp_size = size
        #
        # return tirps

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
                if tirp.size == 1:
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
                        a=2
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
