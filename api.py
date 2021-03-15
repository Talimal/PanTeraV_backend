from flask import Flask,jsonify
from flask_cors import CORS
import main, json
app=Flask(__name__)
CORS(app)


def do_dict(child):
	child.__dict__

[manager,states_map,raw_data] = main.start_project()

@app.route('/startData', methods=['GET'])
def get_start_data():
	# manager = main.start_project()
	start_dict = manager.get_start_dictionary()
	jsonStart={}
	for entry in start_dict:
		array_children = []
		for child in start_dict[entry]:
			array_children.append(json.dumps(child.__dict__))
		jsonStart[json.dumps(entry.__dict__)]=array_children
	return jsonStart

@app.route('/endData', methods=['GET'])
def get_end_data():
	end_dict = manager.get_end_dictionary()
	jsonEnd={}
	for entry in end_dict:
		array_children = []
		for child in end_dict[entry]:
			array_children.append(json.dumps(child.__dict__))
		jsonEnd[json.dumps(entry.__dict__)]=array_children
	return jsonEnd

@app.route('/states', methods=['GET'])
def get_states():
	return json.dumps(states_map)

@app.route('/rawData', methods=['GET'])
def get_raw_data():
	json_raw = {}
	for entity in raw_data:
		array_intervals = []
		for raw_interval in raw_data[entity]:
			array_intervals.append(json.dumps(raw_interval.__dict__))
		json_raw[json.dumps(entity)] = array_intervals
	return json_raw

@app.route('/')
def get():
    return {"haha":" data"}

if __name__ == '__main__':
    app.run(debug=True)
