from flask import Flask,jsonify
from flask_cors import CORS
from Create_Vectors_Index import Create_Vectors_Index
import main, json
app=Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

def do_dict(child):
	child.__dict__

forward_tree,backwards_tree,relations_vectors, tirps = main.start_project(dataset_path="Datasets/ASL")

@app.route('/startData', methods=['GET'])
def get_start_data():
	# manager = main.start_project()
	# start_dict = manager.get_start_dictionary()
	# jsonStart={}
	# for entry in start_dict:
	# 	array_children = []
	# 	for child in start_dict[entry]:
	# 		array_children.append(json.dumps(child.__dict__))
	# 	jsonStart[json.dumps(entry.__dict__)]=array_children
	return None

@app.route('/endData', methods=['GET'])
def get_end_data():
	# end_dict = manager.get_end_dictionary()
	# jsonEnd={}
	# for entry in end_dict:
	# 	array_children = []
	# 	for child in end_dict[entry]:
	# 		array_children.append(json.dumps(child.__dict__))
	# 	jsonEnd[json.dumps(entry.__dict__)]=array_children
	return None

@app.route('/states', methods=['GET'])
def get_states():
	return None

@app.route('/rawData', methods=['GET'])
def get_raw_data():
	# json_raw = {}
	# for entity in raw_data:
	# 	array_intervals = []
	# 	for raw_interval in raw_data[entity]:
	# 		array_intervals.append(json.dumps(raw_interval.__dict__))
	# 	json_raw[json.dumps(entity)] = array_intervals
	return None

@app.route('/')
def get():
    return {"haha":" data"}

@app.route('/forwardTree')
def get_forward_tree():
	json_data = json.dumps(forward_tree, default=lambda o: o.__dict__, indent=4)
	return json_data

@app.route('/backwardsTree')
def get_backwards_tree():
	json_data = json.dumps(backwards_tree, default=lambda o: o.__dict__, indent=4)
	return json_data

@app.route('/vectorSymbols')
def get_vector_symbols():
	json_data = Create_Vectors_Index().get_json_from_data(vectors=relations_vectors)
	a=relations_vectors
	return json_data

@app.route('/tirps')
def get_tirps():
	json_data = json.dumps(tirps, default=lambda o: o.__dict__, indent=4)
	a=json_data
	return json_data


if __name__ == '__main__':
    app.run(debug=True)
