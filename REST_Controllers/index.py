from flask import Flask, jsonify, request
from Analytics import Create_Model, Predictor, Retrieve_Model
import os

app = Flask(__name__)


@app.route("/createmodel")
def create_model():
	algorithm = request.args.get('algorithm')
	sensor_id = request.args.get('sensorid')
	model_name = request.args.get('name')
	print(algorithm)
	print(sensor_id)
	print(model_name)
	if algorithm == 'Regression':
		Create_Model.create_regression_model(model_name, sensor_id)
	elif algorithm == 'Classification':
		Create_Model.create_classification_model(model_name, sensor_id)
	elif algorithm == 'Clustering':
		Create_Model.create_clustering_model(model_name, sensor_id)
	elif algorithm == 'Stream KNN classification':
		snapshots = request.args.get('snapshots')
		print(snapshots)
		Create_Model.create_knn_stream(model_name, sensor_id, int(snapshots))
	elif algorithm == 'Frequent Pattern mining':
		Create_Model.create_fp_model(model_name, sensor_id)
	elif algorithm == 'Stream KMeans Clustering':
		snapshots = request.args.get('snapshots')
		print(snapshots)
		Create_Model.create_kmeans_stream(model_name, sensor_id, int(snapshots))
	elif algorithm == 'Stream Hoeffding Tree Classifier':
		snapshots = request.args.get('snapshots')
		print(snapshots)
		Create_Model.create_hoeffdingtree_stream(model_name, sensor_id, int(snapshots))
	else:
		return 'invalid algorithm selection'

	return "Model created"

@app.route("/getstatistics")
def get_statistics():
	model_name = request.args.get('model_name')
	print(model_name)
	model_stats = Retrieve_Model.get_statistics(model_name)
	print(model_stats)
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

@app.route("/getalgorithms")
def get_algorithms():
	algorithms = ['Regression', 'Classification', 'Clustering', 'Frequent Pattern mining', 'Stream KNN classification', 'Stream KMeans Clustering', 'Stream Hoeffding Tree Classifier']
	dictionary ={}
	dictionary['algorithms'] = algorithms
	algo_json = jsonify(dictionary)
	return algo_json

@app.route("/getmodels")
def get_models():
	files = [f for f in os.listdir('Analytics/Pickle_files')]
	models = []
	for f in files:
		models.append(f)
	saved_models = {}
	print(models)
	saved_models["models"] = models
	models_json = jsonify(saved_models)
	return models_json