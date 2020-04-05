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
        model = Model.fromFile("Analytics/PMML/" + model_name + ".pmml")
        result = model.predict({'X': 95.0, 'Y': 8})
        prediction["result"] = result["prediction"]
    elif model_type == 'Classification':
        model = Model.fromFile("Analytics/PMML/" + model_name + ".pmml")
        result = model.predict({'sepal_length': 2.1, 'sepal_width': 5.5, 'petal_length': 2.4, 'petal_width': 1.0})
        prediction["result"] = result["prediction"]

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

