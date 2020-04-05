import os
import pickle
import time
import pandas as pd

def get_statistics(model_name):
    print('loading file')
    filename = "Analytics/Pickle_files/" + model_name + ".pickle"
    file = open(filename, 'rb')
    model = pickle.load(file)

    model_type = model.type
    statistics = {}
    model_statistics = []
    if model_type == 'Regression':
        statistics["Name"] = model_name
        statistics["Description"] = model.description
        statistics["Mean Square Error"] = model.rmse
        statistics["Execution Time in seconds"] = model.exe_time
        statistics["Data entries analyzed"] = model.data_size
        statistics["Coefficients"] = model.coefficients
        statistics["intercept"] = model.intercept

    elif model_type == 'Classification':
        statistics["Name"] = model_name
        statistics["Description"] = model.description
        statistics["Execution Time in seconds"] = model.exe_time
        statistics["Test Error"] = model.test_error
        statistics["Data entries analyzed"] = model.data_size

    elif model_type == 'Clustering':
        statistics["Name"] = model_name
        statistics["Description"] = model.description
        statistics["silhouette"] = model.silhouette
        statistics["Execution Time in seconds"] = model.exe_time
        statistics["Data entries analyzed"] = model.data_size
        statistics["Cluster centers"] = pd.Series(model.centers).to_json(orient='values')

    elif model_type == 'Stream KNN classification':
        statistics["Name"] = model_name
        statistics["Description"] = model.description
        statistics["Data entries analyzed"] = model.data_size
        statistics["Accuracy"] = model.accuracy

    elif model_type == 'Frequent Pattern mining':
        statistics["Name"] = model_name
        statistics["Description"] = model.description
        statistics["Execution Time in seconds"] = model.exe_time
        statistics["Data entries analyzed"] = model.data_size
        statistics["Frequent Patterns"] = model.frequent_patterns.to_json(orient='values')
        print(model.frequent_patterns)
        statistics["Association Rules"] = model.assocaition_rules.to_json(orient='values')
        print(model.assocaition_rules)
        statistics["Minimum Support"] = model.min_support
        statistics["Minimum Confidence"] = model.min_confidence

    elif model_type == 'Stream KMeans Clustering':
        statistics["Name"] = model_name
        statistics["Description"] = model.description
        statistics["Data entries analyzed"] = model.data_size
        statistics["Cluster centers"] = model.kmeans.cluster_centers_.tolist()

    elif model_type == 'Stream Hoeffding Tree Classifier':
        statistics["Name"] = model_name
        statistics["Description"] = model.description
        statistics["Data entries analyzed"] = model.data_size
        statistics["Accuracy"] = model.accuracy

    else:
        statistics["Error"] = 'Model Not found'

    model_statistics.append(statistics)
    return model_statistics

def getAllModels():
    files = [f for f in os.listdir('Analytics/Pickle_files')]
    models = []
    for f in files:
        prop ={}
        if f != "sample.pickle":
            file = open("Analytics/Pickle_files/" + f, 'rb')
            model = pickle.load(file)
            prop["name"] = f.split('.')[0]
            if "Stream" not in model.type:
                prop["type"] = "Batch"
            else:
                prop["type"] = "Stream"
            prop["algorithm"] = model.type
            prop["time"] = model.time_created
            models.append(prop)

    return models