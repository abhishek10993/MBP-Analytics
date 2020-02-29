from flask import Flask, jsonify, request
from Analytics import Create_Model, Predictor, Retrieve_Model
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


@app.route("/createmodel", methods = ['POST'])
def create_model():
	algorithm = request.args.get('algorithm')
	sensor_id = request.args.get('sensorid')
	model_name = request.args.get('name')
	if algorithm == 'Regression':
		Create_Model.create_regression_model(model_name, sensor_id)
	elif algorithm == 'Classification':
		Create_Model.create_classification_model(model_name, sensor_id)
	elif algorithm == 'Clustering':
		Create_Model.create_clustering_model(model_name, sensor_id)
	elif algorithm == 'Stream KNN classification':
		snapshots = request.args.get('time')
		Create_Model.create_knn_stream(model_name, sensor_id, int(snapshots))
	elif algorithm == 'Frequent Pattern mining':
		Create_Model.create_fp_model(model_name, sensor_id)
	elif algorithm == 'Stream KMeans Clustering':
		snapshots = request.args.get('time')
		Create_Model.create_kmeans_stream(model_name, sensor_id, int(snapshots))
	elif algorithm == 'Stream Hoeffding Tree Classifier':
		snapshots = request.args.get('time')
		Create_Model.create_hoeffdingtree_stream(model_name, sensor_id, int(snapshots))
	else:
		return 'invalid algorithm selection'

	return "Model created"

@app.route("/getstatistics")
def get_statistics():
	model_name = request.args.get('model_name')
	model_stats = Retrieve_Model.get_statistics(model_name)
	stats_json = jsonify(model_stats)
	return stats_json

@app.route("/predictvalue")
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
