from flask import Flask,jsonify
from flask_cors import CORS
import main, json
app=Flask(__name__)
CORS(app)


def do_dict(child):
	child.__dict__

@app.route('/data', methods=['GET'])
def get_data():
	manager = main.start_project()
	start_dict = manager.get_start_dictionary()
	jsonFinal={}
	for entry in start_dict:
		array_children = []
		for child in start_dict[entry]:
			array_children.append(json.dumps(child.__dict__))
		jsonFinal[json.dumps(entry.__dict__)]=array_children
	return jsonFinal


@app.route('/')
def get():
    return {"haha":" data"}

if __name__ == '__main__':
    app.run(debug=True)
