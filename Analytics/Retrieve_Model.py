import os
import pickle
import time

def get_statistics(model_name):
    print('loading file')
    filename = "Analytics/Pickle_files/" + model_name + ".pickle"
    file = open(filename, 'rb')
    model = pickle.load(file)

    model_type = model.type
    statistics = {}
    if model_type == 'Regression':
        statistics["Mean Square Error"] = model.rmse
        statistics["Execution Time in seconds"] = model.exe_time
        statistics["Data entries analyzed"] = model.data_size
        statistics["Coefficients"] = model.coefficients
        statistics["intercept"] = model.intercept

    elif model_type == 'Classification':
        statistics["Execution Time in seconds"] = model.exe_time
        statistics["Test Error"] = model.test_error
        statistics["Data entries analyzed"] = model.data_size

    elif model_type == 'Clustering':
        statistics["silhouette"] = model.silhouette
        statistics["Execution Time in seconds"] = model.exe_time
        statistics["Data entries analyzed"] = model.data_size
        statistics["Cluster centers"] = model.centers

    elif model_type == 'Stream KNN classification':
        statistics["Data entries analyzed"] = model.data_size
        statistics["Accuracy"] = model.accuracy

    elif model_type == 'Frequent Pattern mining':
        statistics["Execution Time in seconds"] = model.exe_time
        statistics["Data entries analyzed"] = model.data_size
        statistics["Frequent Patterns"] = model.frequent_patterns
        statistics["Association Rules"] = model.assocaition_rules

    elif model_type == 'Stream KMeans Clustering':
        statistics["Data entries analyzed"] = model.data_size
        statistics["Cluster centers"] = model.kmeans.cluster_centers_

    elif model_type == 'Stream Hoeffding Tree Classifier':
        statistics["Data entries analyzed"] = model.data_size
        statistics["Accuracy"] = model.accuracy

    else:
        statistics["Error"] = 'Model Not found'

    return statistics

def getAllModels():
    files = [f for f in os.listdir('Analytics/Pickle_files')]
    models = []
    prop = {}
    for f in files:
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
            print(prop)
            time.sleep(2)
            models.append(prop)
    return models