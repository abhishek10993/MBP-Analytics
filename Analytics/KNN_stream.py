import configparser
import requests
from time import gmtime, strftime
from Data_Handlers import Data_Handler_knn
import numpy as np

class KNN_stream:

    accuracy = None
    data_size = None
    correct_predict = None
    knn = None
    type = 'Stream KNN classification'
    time_created = None

    def __init__(self):
        pass

    def create_knn_model(self, kn, size, right, sensor_id):
        self.time_created = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data = Data_Handler_knn.get_data(5)
        feature = []
        status = []
        #print(data)
        for value in data:
            feature.append(value[:3])
            status.append(value[3])
        X = np.ndarray(shape=(5,3), buffer = np.array(feature))
        y = np.array(status)

        self.knn = kn
        #pipeline = PMMLPipeline([("classifier", knn)])
        self.knn.partial_fit(X, y)

        n_samples = size
        corrects = right
        datapoints = 0

        while (True):
            data = Data_Handler_knn.get_data(1)
            X = np.ndarray(shape=(1, 3), buffer=np.array(data[0][:3]))
            y = np.array([data[0][3]])
            my_pred = self.knn.predict(X)
            #print(my_pred, '\n\n')
            if y[0] == my_pred[0]:
                corrects += 1
            self.knn = self.knn.partial_fit(X, y)
            n_samples += 1
            datapoints += 1
            #time.sleep(2)
            if datapoints == 20:
                break

        print('{} samples analyzed.'.format(n_samples))
        print('{} correct.'.format(corrects))
        print("KNN's performance: {}".format(corrects / n_samples))
        self.data_size = n_samples
        self.correct_predict = corrects
        self.accuracy = corrects/n_samples

        #sklearn2pmml(pipeline, "PMML/knn.pmml", with_repr = True)
