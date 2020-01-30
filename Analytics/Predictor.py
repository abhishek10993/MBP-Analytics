from pypmml import Model

def predict_regression():
    model = Model.fromFile("PMML/Regression.pmml")
    result = model.predict({'X': 95.0, 'Y': 8})
    print(result)

def predict_classification():
    model = Model.fromFile("PMML/DecisionTree.pmml")
    result = model.predict({'sepal_length': 2.1, 'sepal_width': 5.5, 'petal_length': 2.4, 'petal_width': 1.0})
    print(result)


predict_classification()
predict_regression()