from Regression import Regression
from FrequentPattern import FrequentPattern
from Clustering import Clustering
from Classification import Classification
import pickle

def create_regression_model():
    regression = Regression()
    regression.perform_regression()

    print(regression.rmse)
    print(regression.coefficients)
    print(regression.intercept)

    with open('Pickle_files/regression.pickle', 'wb') as f:
        pickle.dump(regression, f)

    print('loading file')
    file = open('Pickle_files/regression.pickle', 'rb')
    new = pickle.load(file)

    print(new.rmse)
    print(new.intercept)

def create_fp_model():
    fp = FrequentPattern()
    fp.find_fp()

    with open('Pickle_files/frequentpattern.pickle', 'wb') as f:
        pickle.dump(fp, f)


def create_clustering_model():
    cluster = Clustering()
    cluster.perform_clustering()

    with open('Pickle_files/Clustering.pickle', 'wb') as f:
        pickle.dump(cluster, f)

def create_classification_model():
    classification = Classification()
    classification.perform_classification()

    with open('Pickle_files/classification.pickle', 'wb') as f:
        pickle.dump(classification, f)


create_clustering_model()
