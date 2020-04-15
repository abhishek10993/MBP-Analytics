from flask import Flask, jsonify, request
from Analytics import Create_Model, Predictor, Retrieve_Model
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def checkup():
	return 'Analytics framework running'

@app.route("/createmodel", methods = ['POST'])
#@app.route("/createmodel")
def create_model():
	algorithm = request.args.get('algorithm')
	sensor_id = request.args.get('sensorid')
	model_name = request.args.get('name')
	model_description = request.args.get('description')
	if algorithm == 'Regression':
		Create_Model.create_regression_model(model_name, sensor_id, model_description)
	elif algorithm == 'Classification':
		Create_Model.create_classification_model(model_name, sensor_id, model_description)
	elif algorithm == 'Clustering':
		Create_Model.create_clustering_model(model_name, sensor_id, model_description)
	elif algorithm == 'Stream KNN classification':
		time = request.args.get('time')
		snapshots = int(time * 48)
		Create_Model.create_knn_stream(model_name, sensor_id, snapshots, model_description)
	elif algorithm == 'Frequent Pattern mining':
		Create_Model.create_fp_model(model_name, sensor_id, model_description)
	elif algorithm == 'Stream KMeans Clustering':
		time = request.args.get('time')
		snapshots = int(time * 48)
		Create_Model.create_kmeans_stream(model_name, sensor_id, snapshots, model_description)
	elif algorithm == 'Stream Hoeffding Tree Classifier':
		time = request.args.get('time')
		snapshots = int(time * 48)
		Create_Model.create_hoeffdingtree_stream(model_name, sensor_id, snapshots, model_description)
	else:
		return 'invalid algorithm selection'

	return "Model created"

@app.route("/getstatistics")
def get_statistics():
	model_name = request.args.get('model_name')
	model_stats = Retrieve_Model.get_statistics(model_name)
	stats_json = jsonify(model_stats)
	return stats_json

@app.route("/getprediction")
def get_prediction():
	model_name = request.args.get('model_name')
	value = request.args.get('value')
	print(model_name)
	print(value)
	prediction = Predictor.predict_value(model_name, value)
	predict_json = jsonify(prediction)
	return predict_json

@app.route("/getstreamalgorithms")
def get_stream_algorithms():
	algorithms = [{"id": 1, "name": "Stream KNN classification"},{"id": 2, "name": "Stream KMeans Clustering"},{"id": 3, "name": "Stream Hoeffding Tree Classifier"}]
	algo_json = jsonify(algorithms)
	return algo_json

@app.route("/getbatchalgorithms")
def get_batch_algorithms():
	algorithms = [{"id": 1, "name": "Regression"}, {"id": 2, "name": "Classification"},{"id": 3, "name": "Clustering"},{"id": 4, "name": "Frequent Pattern mining"}]
	algo_json = jsonify(algorithms)
	return algo_json

@app.route("/getmodels")
def get_models():
	models = Retrieve_Model.getAllModels()
	models_json = jsonify(models)
	#print(models_json)
	return models_json

@app.route("/deletemodel", methods = ['DELETE'])
def delete_model():
	model_name = request.args.get('model_name')
	try:
		os.remove("Analytics/Pickle_files/" + model_name + ".pickle")
		os.remove("Analytics/PMML/" + model_name + ".pmml")
	except FileNotFoundError:
		print('File not found')

	return 'Success'
