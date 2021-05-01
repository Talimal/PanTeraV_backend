import json
from Visualization.Tali.relations_vector import Relations_Vector
from Visualization.Tali.TIRP import TIRP
# from relations_vector import Relations_Vector
from types import SimpleNamespace

class Create_Vectors_Index (object):

    def __init__(self, relations_vectors=None, vectors_index_path=""):
        # output index file path
        if vectors_index_path!="":
            self.index_file = open(vectors_index_path, "w")

        self.relations_vectors = relations_vectors

        # creating the index output file
        self.vectors_index_path = vectors_index_path
        if relations_vectors is not None:
            self.serialize_vectors(self.relations_vectors)
            self.index_file.close()

            self.deserialize_vectors()

    """the relation_vector object is too complicated to be serialized to file
        so i casting it to a json that the key is a string of the symbol with the relations
        (because tuple is not serialized in python)
        and the value is the serialization of the object itself (the method relation_vector.serialize is in the class
        relation_vector."""
    def remap_keys(self, data):
        new_json={}
        for (symbol,relations) in data:
            relation_vector=data[(symbol,relations)]
            """turning the structure of the original json to a string key and serialized value"""
            new_json[str(symbol)+","+self.get_string_from_array(relations)] = relation_vector.serialize()
        return new_json

    """this method gets an array of any kind and returns a string representation of it's elements one after the other
        seperated by ','"""
    def get_string_from_array(self, array):
        final_string = ""
        for element in array:
            final_string = final_string + str(element) + ","
        return final_string[:-1]

    def get_json_from_data(self,vectors):
        a = self.remap_keys(vectors)
        json_data = json.dumps(a, default=lambda o: o.__dict__, indent=4)
        return json_data

    """this method gets the original json of key: (symbol,relations) value: relation_vector object and
        serialize it to an index file"""
    def serialize_vectors(self,vectors):
        json_data = self.get_json_from_data(vectors=vectors)
        self.index_file.write(json_data)

    """this method gets a relation_vector object and returns it (symbol,relations) as tuple"""
    def get_symbol_and_relations_of_vector(self, vector):
        symbol_relations_arr = vector.split(',')
        symbol = int(symbol_relations_arr[0])
        if symbol_relations_arr[1] == '':
            relations_ = []
        else:
            relations_ = symbol_relations_arr[1:]
        return symbol, relations_

    """this method gets a json that is either a prefix json or next json (see fields of relations_vector)
        the method returns a json key:(symbol,relations) value: all the tirps that ends with / stars with the key
        exactly like the json object in the Read_KL_Output_File.py"""
    def get_json_of_vector(self, symbol_tirps_json):
        relation_tirp_json = {}
        for relation_tirp in symbol_tirps_json:
            key = relation_tirp.split(',')
            symbol = int(key[0])
            if key[1] == '':
                relations = []
            else:
                relations = key[1:]
            tirps_json_list = symbol_tirps_json[relation_tirp]
            tirps_list = []
            for tirp in tirps_json_list:
                new_tirp = TIRP(**json.loads(json.dumps(tirp)))
                tirps_list.append(new_tirp)

            relation_tirp_json[(symbol, tuple(relations))] = tirps_list
        return relation_tirp_json

    """this method openes the index file and deserialized the json object there.
        the json object in the file represents the json object in Read_KL_Output_File.py"""
    def deserialize_vectors(self):
        with open(self.vectors_index_path, "r") as my_file_read:
            index_content = json.dumps(json.load(my_file_read))
            index_json = json.loads(index_content)
            relations_vectors_json = {}

            for vector in index_json:
                symbol_vector, relations_vector = self.get_symbol_and_relations_of_vector(vector=vector)
                prefix_json = self.get_json_of_vector(symbol_tirps_json=index_json[vector]['prefix'])
                next_json = self.get_json_of_vector(symbol_tirps_json=index_json[vector]['next'])
                vector = Relations_Vector(symbol=symbol_vector,relation_vector=relations_vector,prefix_tirps=prefix_json,next_tirps=next_json)
                relations_vectors_json[(vector.get_symbol(), tuple(vector.get_relation_vector()))] = vector
        return relations_vectors_json
