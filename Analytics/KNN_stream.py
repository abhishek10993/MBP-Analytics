import configparser
import requests
from skmultiflow.lazy import KNN
import time
from Data_Handlers import Data_Handler_knn
import numpy as np

class KNN_stream:

    def __init__(self):
        pass

    def create_knn_model(self):
        data = Data_Handler_knn.get_data(5)
        feature = []
        status = []
        #print(data)
        for value in data:
            feature.append(value[:3])
            status.append(value[3])
        print(feature)
        print(status)
        X = np.ndarray(shape=(5,3), buffer = np.array(feature))
        y = np.array(status)
        print(X, "**")
        print(y, "**")

        knn = KNN()
        #pipeline = PMMLPipeline([("classifier", knn)])
        knn.partial_fit(X, y)

        n_samples = 0
        corrects = 0

        while (True):
            data = Data_Handler_knn.get_data(1)
            X = np.ndarray(shape=(1, 3), buffer=np.array(data[0][:3]))
            print(X, "**")
            y = np.array([data[0][3]])
            print(y, "**")
            my_pred = knn.predict(X)
            print(my_pred, '\n\n')
            if y[0] == my_pred[0]:
                corrects += 1
            knn = knn.partial_fit(X, y)
            n_samples += 1
            #time.sleep(2)
            if n_samples == 20:
                break

        print('{} samples analyzed.'.format(n_samples))
        print('{} correct.'.format(corrects))
        print("KNN's performance: {}".format(corrects / n_samples))

        #sklearn2pmml(pipeline, "PMML/knn.pmml", with_repr = True)

    create_knn_model()