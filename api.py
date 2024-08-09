from flask import current_app, g
import Create_Indexes
import Read_KL_Output_File
from math import factorial


import json
import os
COUNTER_FOR_LOAD = "0"
TIRPS_INDEX_FILE = "TIRPs_index.json"
SYMBOL_TIRPS = "symbol_TIRPs"
PROPERTIES = "properties_TIRPs.json"
RAW_DATA_INDEX = "raw_data_index"
DESCRITE_DATA_INDEX = "descrite_data_index"
TIRPS_JSON = "TIRPs_json.json"


def initialize(dataset_name, visualization_path):
    path = os.path.dirname(os.path.abspath(__file__))
    symbol_tirps_path = os.path.join(path, "datasets", SYMBOL_TIRPS)
    if not os.path.exists(symbol_tirps_path):
        symbol_TIRPs, symbols_to_names = Read_KL_Output_File.initialize_read_file()
        # serializing to index files, the return value is not interesting
        symbol_TIRPs = Create_Indexes.create_symbol_TIRPs_index(symbol_TIRPs=symbol_TIRPs)
        current_app.logger.debug("TALI PREPROCESSING - index for symbol tirps")
        symbols_to_names = Create_Indexes.create_symbols_names_index(symbols_to_names=symbols_to_names)
        current_app.logger.debug("TALI PREPROCESSING - created index for symbols names")
        # create a file with name 'finished' as indication for later
        indicate_finished(visualization_path="datasets", dataset_name=dataset_name)
       


"""creates the file with the name 'finished' as indication for finished preprocessing"""
def indicate_finished(dataset_name, visualization_path):
    dataset_path = "datasets"
    path = os.path.join(dataset_path, "finished")
    with open(path, "w") as file:
        file.write("finished")


def get_symbol_TIRPs(dataset_name, visualization_path):
    symbol_TIRPs = Create_Indexes.create_symbol_TIRPs_index(symbol_TIRPs={})
    return json.dumps(symbol_TIRPs)


def get_tirps_json(dataset_name, visualization_path):
    dataset_path = None
    tirps = Create_Indexes.create_TIRPs_json_index(visualization_path=dataset_path, tirps_json=[])
    return json.dumps(tirps)

def get_symbols_names(dataset_name, visualization_path):
    symbols_names = Create_Indexes.create_symbols_names_index(symbols_to_names={})
    return json.dumps(symbols_names)

def get_correlated_symbols(dataset_name, visualization_path):
    dataset_path = os.path.join(
        current_app.config["DATASETS_ROOT"], dataset_name, "Visualizations", visualization_path
    )
    correlated_symbols = Create_Indexes.create_correlation_json(visualization_path=dataset_path, correlation_symbols={})
    return json.dumps(correlated_symbols)



def get_more_raw_data(self):
    # json_data = self.raw_class.get_more_raw_data(self.dataset_path)
    # return json_data
    return ""

def get_supporting(tirp_name, visualizationid, dataset_name):
    name = tirp_name.split("|")[0].split("-")
    relation = tirp_name.split("|")[1].split(".")
    if (os.path.exists(os.path.join(
        current_app.config["DATASETS_ROOT"], dataset_name, "visualizations", visualizationid, "chunks_with_entities", name[0] + ".json"
    ))):
        path_to_tirp_entities = os.path.join(
        current_app.config["DATASETS_ROOT"], dataset_name, "visualizations", visualizationid, "chunks_with_entities", name[0] + ".json"
        )
    else:
        return
    with open(path_to_tirp_entities) as file:
        entities = json.load(file)
        supporting = {}
        index = 0
        found = False
        ent = entities
        while True:
            # if ent["symbols"] == name and ent["relations"] == relation:
            #     found = True
            # else:
            if relation[0] == '' and ent["symbols"] == name:
                break
            if ent["symbols"] == name and ent["relations"] == relation:
                    break
            else:
                for child in ent["children"]:
                    
                    if len(child["relations"]) == 1:
                        combination = 1
                    else:
                        combination = int(factorial(len(child["relations"]))/(factorial(2)*factorial(len(child["relations"])-2)))
                    # print("origin:" + str(relation[:combination]))
                    # print("child:" + str(child["relations"]))
                    # print(child["relations"] == relation[:combination])
                    if child["symbols"] == name[:len(child["symbols"])] and child["relations"] == relation[:combination]:
                        ent = child
                        break
        # while entities["symbols"] != name and entities["symbols"] !=:
        #     children = entities["children"]
        #     for k in range(len(children)):
        #         if children[k]["symbols"] == name[:index+1] and children[k]["relations"] == relation[:index+1]:
        #             entities = children[k]
            
        #     index +=1
        descrite_entities = {}
        tmp_list = list(ent["stats_cls0"]["entities"].items())
        print(ent["stats_cls0"].items())
        for i in tmp_list:
            descrite_entities[i[0]] = i[1]
        ent = [list(map(lambda x : {"id":x,"name":x}, list(ent["stats_cls0"]["entities"].keys()))), descrite_entities, list(ent["relations"])]

        return json.dumps(ent)


def get_symbols_values_data(dataset_name, visualizationid):
    # json_data = self.raw_class.get_values_data(self.dataset_path)
    # return json_data
    if (os.path.exists(os.path.join(
        current_app.config["DATASETS_ROOT"], dataset_name, "visualizations", visualizationid, "Tali", "symbols_to_names.json"
    ))):
        path = os.path.join(
        current_app.config["DATASETS_ROOT"], dataset_name, "visualizations", visualizationid, "Tali", "symbols_to_names.json"
        )
    else:
        return
    if (os.path.exists(os.path.join(
        current_app.config["DATASETS_ROOT"], dataset_name, "visualizations", visualizationid, "states.json"
    ))):
        path_to_temporal = os.path.join(
        current_app.config["DATASETS_ROOT"], dataset_name, "visualizations", visualizationid, "states.json"
        )
    else:
        return

    dct ={}
    name_symbol={}
    with open(path_to_temporal) as file:
        temporal = json.load(file)
    with open(path) as file:
        states = json.load(file)
        for i in states:
            name_symbol[states[i]] = i
    for i in temporal:
        dct[states[i["StateID"]]] = [i["TemporalPropertyID"],i["BinLow"],i["BinHigh"]]
    return {"state_temporal":dct, "name_symbol":name_symbol}

