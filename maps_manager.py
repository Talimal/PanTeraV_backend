
"""class that is responsible for holding for each TIRP, the tirps that come befoore and after it (only one level at time)
    for example TIRP in size 2 , will have TIRPS in size 1 that come before it and TIRPS in size 3 that come after it"""

class maps_manager (object):

    def __init__(self, tirps):
        self.start_dictionary = dict()
        self.come_before = dict()
        self.end_dictionary = dict()
        self.tirps = tirps
        self.init_dictionaries()
        self.build_start_dictionary()
        self.build_end_dictionary()
        self.raw_intervals = dict()



    """returns the dictionary- key[TIRP]:value - list of TIRPS that come after it"""
    def get_start_dictionary(self):
        return self.start_dictionary

    def get_come_before_dictionary(self):
        return self.come_before

    """returns the dictionary- key[TIRP]:value - list of TIRPS that come before it"""
    def get_end_dictionary(self):
        return self.end_dictionary

    """initiates location for each TIRP in every dictionary"""
    def init_dictionaries(self):
        for tirp in self.tirps:
            self.start_dictionary[tirp] = list()
            self.come_before[tirp] = list()
            self.end_dictionary[tirp] = list()

    """returns all the TIRPS in the start_dic that are in the specific size"""
    def get_start_tirps_by_size(self, tirp_size):
        tirps = list()
        for tirp in self.start_dictionary:
            if tirp.get_size() == tirp_size:
                tirps.append(tirp)
        return tirps

    """returns all the TIRPS in the end_dic that are in the specific size"""
    def get_end_tirps_by_size(self, tirp_size):
        tirps = list()
        for tirp in self.end_dictionary:
            if tirp.get_size() == tirp_size:
                tirps.append(tirp)
        return tirps

    """returns all the TIRPS that start in specific TIRP (come after it)"""
    def get_starts_by_tirp(self, tirp):
        return self.start_dictionary[tirp]

    """returns all the TIRPS that end in specific TIRP (come before it)"""
    def get_ends_by_tirp(self, tirp):
        return self.end_dictionary[tirp]



    def build_start_dictionary(self):
        for tirp in self.tirps:
            # if tirp size if 1, there is no tirps from left(before it), then continue
            tirp_size = tirp.get_size()
            if tirp_size == 1:
                continue

            # n is the size of the risha:

            n=tirp_size-1
            #get all the TIRPs in size of risha
            tirps_in_size_n = self.get_start_tirps_by_size(tirp_size=n)
            #get all the TIRPs in size of risha with the same symbols as the current TIRP
            risha_symbols = tirp.get_symbols()[0:n]
            tirps_with_symbols = self.get_tirps_by_symbols(tirps_list=tirps_in_size_n, symbol_list=risha_symbols)
            #from all the TIRPs till now, get the ones with the same relations as the current TIRP
            num_relations = int((n)*(n-1)/2) # n=size-1
            risha_relations=[]
            if num_relations>0:
                risha_relations = tirp.get_relations()[0:num_relations]

            risha_tirps = self.get_tirps_by_relations(tirps_list=tirps_with_symbols, relation_list=risha_relations)
            #add the current TIRP from the right to all the risha TIRPs
            self.add_tirp_to_start_by_tirplist(tirps_list=risha_tirps, tirp_to_add=tirp)
            self.add_before_tirps_by_tirp(tirp=tirp, before_tirp_list=risha_tirps)

    """return all the tirps in the list that has the same symbol list as given"""
    def get_tirps_by_symbols(self, tirps_list, symbol_list):
        tirps_with_same_symbols = list()
        for tirp in tirps_list:
            # check if tirps symbols are the ones we are looking for
            if tirp.get_symbols() == symbol_list:
                tirps_with_same_symbols.append(tirp)
        return tirps_with_same_symbols

    """return all the tirps in the list that has the same relations as given"""
    def get_tirps_by_relations(self, tirps_list, relation_list):
        tirps_with_same_relations = list()
        for tirp in tirps_list:
            # check if tirps relations are the ones we are looking for
            if tirp.get_relations() == relation_list:
                tirps_with_same_relations.append(tirp)
        return tirps_with_same_relations

    """adds the tirp_to_add at each value in starts_dic for every tirp in tirps_list"""
    def add_tirp_to_start_by_tirplist(self, tirps_list ,tirp_to_add):
        for tirp in tirps_list:
            self.start_dictionary[tirp].append(tirp_to_add)

    """adds the risha tirps as tirps that come before tirp"""
    def add_before_tirps_by_tirp(self, tirp, before_tirp_list):
        for before_tirp in before_tirp_list:
            self.come_before[tirp].append(before_tirp)


    """for every tirp in start_dic, all it's values-big tirps, add this tirp to their end_dic"""
    def build_end_dictionary(self):
     for tirp in self.start_dictionary:
         tirp_size = tirp.get_size()
         n=tirp_size
         end_tirp_size=tirp_size-1
         if end_tirp_size==0:
             continue
         else:
             smaller_end_tirps = self.get_start_tirps_by_size(tirp_size=end_tirp_size)
             symbol_list = tirp.get_symbols()[1:n]
             tirps_symbols = self.get_tirps_by_symbols(tirps_list=smaller_end_tirps,symbol_list=symbol_list)
             number_relations = int((n-1)*(n-2)/2)
             sifa_relations = []
             if number_relations>0:
                sifa_relations = tirp.get_relations()[n-number_relations:n]
             tirps_relations = self.get_tirps_by_relations(tirps_list=tirps_symbols,relation_list=sifa_relations)
             for sifa_tirp in tirps_relations:
                 self.end_dictionary[sifa_tirp].append(tirp)


    def save_raw_inteval(self,entity_id,interval):
        if entity_id in self.raw_intervals:
            self.raw_intervals[entity_id].append(interval)
        else:
            self.raw_intervals[entity_id]=[interval]

    def get_raw_intervals(self):
        return self.raw_intervals