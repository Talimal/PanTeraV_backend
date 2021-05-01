from flask import Flask,jsonify
from flask_cors import CORS
from Visualization.Tali.Create_Vectors_Index import Create_Vectors_Index
# from Create_Vectors_Index import Create_Vectors_Index
import Visualization.Tali.Tali_main, json
from Visualization.Tali import Tali_main as main
app=Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})




class Tali_api(object):

		def __init__(self,dataset_path):
			self.dataset_path = dataset_path
			forward_tree, backwards_tree, relations_vectors, tirps = main.start_project(dataset_path=self.dataset_path)
			self.forward_tree = forward_tree
			self.backwards_tree = backwards_tree
			self.relations_vectors = relations_vectors
			self.tirps = tirps


		def get_forward_tree(self):
			json_data = json.dumps(self.forward_tree, default=lambda tirp: tirp.serialize(), indent=4)
			return json_data

		def get_backwards_tree(self):
			json_data = json.dumps(self.backwards_tree, default=lambda tirp: tirp.serialize(), indent=4)
			return json_data

		def get_vector_symbols(self):
			json_data = Create_Vectors_Index().get_json_from_data(vectors=self.relations_vectors)
			a=self.relations_vectors
			return json_data

		def get_tirps(self):
			json_data = json.dumps(self.tirps, default=lambda tirp: tirp.serialize(), indent=4)
			a=json_data
			return json_data
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
