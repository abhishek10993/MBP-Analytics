from Regression import Regression
from FrequentPattern import FrequentPattern
import pickle

def create_regression_model():
    obj = Regression()
    obj.perform_regression()

    print(obj.rmse)
    print(obj.coefficients)
    print(obj.intercept)

    with open('Pickle_files/mypickle.pickle', 'wb') as f:
        pickle.dump(obj, f)

    print('loading file')
    file = open('Pickle_files/mypickle.pickle', 'rb')
    new = pickle.load(file)

    print(new.rmse)
    print(new.intercept)

def create_fp_model():
    obj = FrequentPattern()
    obj.find_fp()


create_fp_model()
