import pickle
import numpy as np
from pypmml import Model

def predict_value(model_name, value):

    filename = "Analytics/Pickle_files/" + model_name + ".pickle"
    file = open(filename, 'rb')
    model = pickle.load(file)
    model_type = model.type
    prediction = {}
    predicted_value = []
    if model_type == 'Regression':
        model_pmml = Model.fromFile("Analytics/PMML/" + model_name + ".pmml")
        features = model.features
        data = value.split(',')
        to_predict = {}
        try:
            for i in range(len(data)):
                to_predict[features[i]] = data[i]
            print(to_predict)
            result = model_pmml.predict(to_predict)
            prediction["result"] = result["prediction"]
        except:
            prediction["result"] = "Error"

    elif model_type == 'Classification':
        model_pmml = Model.fromFile("Analytics/PMML/" + model_name + ".pmml")
        features = model.features
        data = value.split(',')
        to_predict = {}
        try:
            for i in range(len(data)):
                to_predict[features[i]] = data[i]
            print(to_predict)
            result = model_pmml.predict(to_predict)
            prediction["result"] = result["prediction"]
        except:
            prediction["result"] = "Error"

    elif model_type == 'Stream KNN classification':
        data = value.split(',')
        predict =[]
        for point in data:
            predict.append(float(point))
        X = np.ndarray(shape=(1, len(predict)), buffer=np.array(predict))
        pred = model.knn.predict(X)
        prediction["result"] = float(pred[0])
    elif model_type == 'Stream Hoeffding Tree Classifier':
        data = value.split(',')
        predict = []
        for point in data:
            predict.append(float(point))
        X = np.ndarray(shape=(1, len(predict)), buffer=np.array(predict))
        pred = model.hoeffding_tree.predict(X)
        prediction["result"] = float(pred[0])

    else:
        prediction["Error"] = 'Model Not found'

    predicted_value.append(prediction)
    return predicted_value

