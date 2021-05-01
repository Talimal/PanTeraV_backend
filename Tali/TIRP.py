import statistics
import math

class TIRP (object):

    def __init__(self, size, symbols, relations, num_supporting_entities, mean_horizontal_support, occurences, supporting_instances=list(),
                                                                mean_of_first_interval=0.0,mean_offset_from_first_symbol=list(),build_supporting_instances=False,symbols_names=[]):
        self.__size = size
        self.__symbols = symbols
        self.__relations = relations
        self.__num_supporting_entities = num_supporting_entities
        self.__mean_horizontal_support = mean_horizontal_support
        self.__occurences = occurences
        self.__supporting_instances = supporting_instances
        """average duration of first symbol in TIRP"""
        self.__mean_of_first_interval = mean_of_first_interval
        """array that every pair of cells: [offset from start of first interval, offset from end of first interval]"""
        self.__mean_offset_from_first_symbol = []
        self.build_supporting_instances=build_supporting_instances
        self.__symbols_names = []

        # self.hs_confidence_interval_low = 0
        # self.hs_confidence_interval_high = 0
        # self.md_confidence_interval_low = 0
        # self.md_confidence_interval_high = 0
        self.set_supporting_instances(supporting_instances)

    def get_symbols(self):
        return self.__symbols

    def get_size(self):
        return self.__size

    def get_relations(self):
        return self.__relations

    def get_mean_horizontal_support(self):
        return self.__mean_horizontal_support

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
    def string_relations(self, relations):
        if len(relations)>0:
            str = relations[0]+"."
            for i in range(1,len(relations),1):
                str = str+relations[i]+"."
            return str
        else:
            return ""

    def get_vector_in_size(self, vector_size):
        vector_symbol = []
        sum_relations_till_now = 0
        index_symbol = vector_size
        for index in range(0, index_symbol):
            vector_symbol.append(self.__relations[sum_relations_till_now + index_symbol - index - 1])
            sum_relations_till_now += index_symbol - index
        return vector_symbol

    def set_supporting_instances(self,supporting_instances):
        if self.build_supporting_instances:
            for instance in supporting_instances:
                duration_of_instance = 0
                mean_offset_from_first_symbol_of_instance = list()
                for symbolic in instance.get_symbolic_intervals():
                    j = 0
                    # counter = counter + 1
                    end_time_of_first_symbol = symbolic[0].getEndTime()
                    for i in range(0, self.__size):
                        start_time = symbolic[i].getStartTime()
                        end_time = symbolic[i].getEndTime()
                        if i == 0:
                            duration = int(end_time) - int(start_time)
                            # self.__mean_of_first_interval += duration
                            duration_of_instance += duration
                        diff_from_start = int(start_time) - int(end_time_of_first_symbol)
                        diff_from_end = int(end_time) - int(end_time_of_first_symbol)
                        if len(mean_offset_from_first_symbol_of_instance) < j + 1:
                            # self.__mean_offset_from_first_symbol.append(diff_from_start)
                            mean_offset_from_first_symbol_of_instance.append(diff_from_start)
                            mean_offset_from_first_symbol_of_instance.append(diff_from_end)
                            # self.__mean_offset_from_first_symbol.append(diff_from_end)
                        else:
                            mean_offset_from_first_symbol_of_instance[j] += diff_from_start
                            mean_offset_from_first_symbol_of_instance[j + 1] += diff_from_end
                        j = j + 2
                self.__mean_of_first_interval += duration_of_instance / len(instance.get_symbolic_intervals())
                for i in range(0, len(mean_offset_from_first_symbol_of_instance)):
                    mean_offset_from_first_symbol_of_instance[i] = mean_offset_from_first_symbol_of_instance[i] / len(
                        instance.get_symbolic_intervals())
                    if len(self.__mean_offset_from_first_symbol) < i + 1:
                        self.__mean_offset_from_first_symbol.append(mean_offset_from_first_symbol_of_instance[i])
                    else:
                        self.__mean_offset_from_first_symbol[i] += mean_offset_from_first_symbol_of_instance[i]
            # make it mean
            if len(supporting_instances) > 0:
                # self.__mean_of_first_interval = round(self.__mean_of_first_interval / counter, 2)
                self.__mean_of_first_interval = round(self.__mean_of_first_interval / len(supporting_instances), 2)
            for i in range(0, len(self.__mean_offset_from_first_symbol)):
                # self.__mean_offset_from_first_symbol[i] = round(self.__mean_offset_from_first_symbol[i] / counter, 2)
                self.__mean_offset_from_first_symbol[i] = round(
                    self.__mean_offset_from_first_symbol[i] / len(supporting_instances), 2)


    def __str__(self):
        a=self.convert_list_to_string(self.__occurences)
        return "(" + str(self.__size) + ", " + self.string_symbols(self.__symbols) + ", " + \
               self.string_relations(self.__relations) + ", " + self.__num_supporting_entities + ", " + self.__mean_horizontal_support + ", " + \
               self.convert_list_to_string(self.__occurences) + ")"

    def set_symbols_names(self,symbols_names):
        self.__symbols_names = symbols_names

    def get_json_from_field(self,list_instances):
        result = []
        for instance in list_instances:
            result.append(instance.serialize())
        return result

    def serialize(self):
        return {
            'size': self.__size,
            'symbols': self.__symbols,
            'symbols_names': self.__symbols_names,
            'relations': self.__relations,
            'num_supporting_entities': self.__num_supporting_entities,
            'mean_horizontal_support': self.__mean_horizontal_support,
            'occurences': self.__occurences,
            'mean_of_first_interval': self.__mean_of_first_interval,
            'mean_offset_from_first_symbol': self.__mean_offset_from_first_symbol,
            'build_supporting_instances': False
        }
