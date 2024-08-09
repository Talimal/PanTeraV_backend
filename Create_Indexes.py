import json
import os

TIRPS_INDEX_FILE = "TIRPs_index.json"
SYMBOL_TIRPS = "symbol_TIRPs"
PROPERTIES = "properties_TIRPs.json"
TIRPS_JSON = "TIRPs_json.json"
SYMBOLS_NAMES_JSON = "symbols_to_names.json"


"""returns all the TIRPs from their index file after deserializing them"""
def deserialize_tirps():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "datasets", TIRPS_INDEX_FILE)
    with open(path) as file:
        return json.load(file)


"""creates a directory which contains a file for each symbol. in each file there are all the symbols and TIRPS connect the
current symbol to the other symbols (that come before and after it"""
def create_symbol_TIRPs_index(symbol_TIRPs={}):
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "datasets", SYMBOL_TIRPS)

    if os.path.exists(path):
        return deserialize_symbol_TIRPs(path)
    else:
        if symbol_TIRPs == {}:
            raise Exception("you should give symbols TIRPs to create index")
        os.mkdir(path)
        serialized_json_to_send = {}
        for symbol in symbol_TIRPs:
            symbol_next = symbol_TIRPs[symbol]["next"]
            symbol_prefix = symbol_TIRPs[symbol]["prefix"]
            final_json = {}
            next_json = {}
            prefix_json = {}

            for next_symbol in symbol_next:
                tirps = symbol_next[next_symbol]
                serialized_tirps = [tirp.serialize() for tirp in tirps]
                next_json[next_symbol] = serialized_tirps
            for prefix_symbol in symbol_prefix:
                tirps = symbol_prefix[prefix_symbol]
                serialized_tirps = [tirp.serialize() for tirp in tirps]
                prefix_json[prefix_symbol] = serialized_tirps
            final_json["next"] = next_json
            final_json["prefix"] = prefix_json
            serialized_json = json.dumps(final_json, default=lambda o: o.__dict__, indent=4)
            with open(path + "\\" + symbol, "w") as file:
                file.write(serialized_json)

            serialized_json_to_send[symbol] = {"next": next_json, "prefix": prefix_json}
        return serialized_json_to_send


def create_TIRPs_json_index(tirps_json={}):
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "datasets", TIRPS_JSON)

    if os.path.exists(path):
        return deserialize_tirps_json()
    else:
        serialized_json_to_send = {}
        for tirp_name in tirps_json:
            tirp_obj = tirps_json[tirp_name]
            serialized_json_to_send[tirp_name] = tirp_obj.serialize()
        serialized_json = json.dumps(
            serialized_json_to_send, default=lambda o: o.__dict__, indent=4
        )
        with open(path, "w") as file:
            file.write(serialized_json)
        return serialized_json_to_send


def create_symbols_names_index(symbols_to_names={}):
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "datasets", SYMBOLS_NAMES_JSON)
    if os.path.exists(path):
        return deserialize_symbols_to_names()
    else:
        if symbols_to_names == {}:
            raise Exception("you should give symbols names to create index")
        serialized_json = json.dumps(
            symbols_to_names, default=lambda o: o.__dict__, indent=4
        )
        with open(path, "w") as file:
            file.write(serialized_json)
        return symbols_to_names


def deserialize_tirps_json():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "datasets", TIRPS_JSON)
    with open(path) as file:
        return json.load(file)


"""goes to the index directory and the files and deserializes the data and stores it as class fields"""
def deserialize_symbol_TIRPs(visualization_path):
    final_json = {}
    for filename in os.listdir(visualization_path):
        with open(os.path.join(visualization_path, filename)) as file:
            index_json = json.load(file)
            symbol = filename
            final_json[symbol] = index_json
    return final_json

def deserialize_symbols_to_names():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "datasets", SYMBOLS_NAMES_JSON)
    with open(path) as file:
        return json.load(file)


def create_properties_index(visualization_path, props={}):
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "datasets", PROPERTIES)
    final_json = {}
    for prop in props:
        final_json[prop] = []
        for tirp in props[prop]:
            serialized_tirp = tirp.serialize()
            final_json[prop].append(serialized_tirp)
    tali_dir = os.path.join(visualization_path, "Tali")
    if not (os.path.exists(tali_dir)):
        os.mkdir(tali_dir)
    with open(path, "w") as file:
        final_json_to_write = json.dumps(final_json, default=lambda o: o.__dict__, indent=4)
        file.write(final_json_to_write)
    return final_json


"""goes to the index directory and the files and deserializes the data and stores it as class fields"""
def deserialize_properties():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "datasets", PROPERTIES)
    with open(path) as file:
        properties_json = json.dumps(json.load(file))
        properties_json = json.loads(properties_json)
    return properties_json