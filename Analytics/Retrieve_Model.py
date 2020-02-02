import pickle
import numpy as np

def get_statistics(model_name):
    print('loading file')
    filename = "Analytics/Pickle_files/" + model_name + ".pickle"
    file = open(filename, 'rb')
    new = pickle.load(file)

    model_type = new.type
    statistics = {}
    if model_type == 'Regression':
        statistics["Mean Square Error"] = new.rmse
        statistics["Execution Time in seconds"] = new.exe_time
        statistics["Data entries analyzed"] = new.data_size
        statistics["Coefficients"] = new.coefficients
        statistics["intercept"] = new.intercept

    elif model_type == 'Classification':
        statistics["Execution Time in seconds"] = new.exe_time
        statistics["Test Error"] = new.test_error
        statistics["Data entries analyzed"] = new.data_size

    elif model_type == 'Clustering':
        statistics["silhouette"] = new.silhouette
        statistics["Execution Time in seconds"] = new.exe_time
        statistics["Data entries analyzed"] = new.data_size
        statistics["Cluster centers"] = new.centers

    elif model_type == 'Stream KNN classification':
        statistics["Data entries analyzed"] = new.data_size
        statistics["Accuracy"] = new.accuracy

    elif model_type == 'Frequent Pattern mining':
        statistics["Execution Time in seconds"] = new.exe_time
        statistics["Data entries analyzed"] = new.data_size
        statistics["Frequent Patterns"] = new.frequent_patterns
        statistics["Association Rules"] = new.assocaition_rules

    elif model_type == 'Stream KMeans Clustering':
        statistics["Data entries analyzed"] = new.data_size
        statistics["Cluster centers"] = new.kmeans.cluster_centers_

    elif model_type == 'Stream Hoeffding Tree Classifier':
        statistics["Data entries analyzed"] = new.data_size
        statistics["Accuracy"] = new.accuracy

    else:
        statistics["Error"] = 'Model Not found'

    return statistics
