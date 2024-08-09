from flask import current_app
import Create_Indexes
import Read_KL_Output_File
import json
import os

SYMBOL_TIRPS = "symbol_TIRPs"
TIRPS_JSON = "TIRPs_json.json"
DATASETS = "datasets"
FINISHED = "finished"


def initialize():
    path = os.path.dirname(os.path.abspath(__file__))
    symbol_tirps_path = os.path.join(path, DATASETS, SYMBOL_TIRPS)
    if not os.path.exists(symbol_tirps_path):
        symbol_TIRPs, symbols_to_names = Read_KL_Output_File.initialize_read_file()
        symbol_TIRPs = Create_Indexes.create_symbol_TIRPs_index(symbol_TIRPs=symbol_TIRPs)
        current_app.logger.debug("TALI PREPROCESSING - index for symbol tirps")
        symbols_to_names = Create_Indexes.create_symbols_names_index(symbols_to_names=symbols_to_names)
        current_app.logger.debug("TALI PREPROCESSING - created index for symbols names")
        indicate_finished()
       


"""creates the file with the name 'finished' as indication for finished preprocessing"""
def indicate_finished():
    path = os.path.join(DATASETS, FINISHED)
    with open(path, "w") as file:
        file.write(FINISHED)


def get_symbol_TIRPs():
    symbol_TIRPs = Create_Indexes.create_symbol_TIRPs_index(symbol_TIRPs={})
    return json.dumps(symbol_TIRPs)


def get_tirps_json():
    tirps = Create_Indexes.create_TIRPs_json_index(tirps_json=[])
    return json.dumps(tirps)


def get_symbols_names():
    symbols_names = Create_Indexes.create_symbols_names_index(symbols_to_names={})
    return json.dumps(symbols_names)