from time import gmtime, strftime
from Data_Handlers import Stream_Classification_data
import numpy as np
import time
import configparser

class KNN_stream:

    accuracy = None
    data_size = None
    correct_predict = None
    knn = None
    type = 'Stream KNN classification'
    time_created = None
    description = None

    def __init__(self):
        pass

    def create_knn_model(self, kn, size, right, sensor_id, model_description):
        self.time_created = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.description = model_description
        start_time = time.time()
        config = configparser.RawConfigParser()
        config.read('resources/misc.properties')
        time_to_run = int(config.get('TIME', 'streamsave')) * 60
        data = Stream_Classification_data.get_data(sensor_id, 5)
        feature = []
        status = []
        number_of_features = len(data[0])-1
        for value in data:
            feature.append(value[:number_of_features])
            status.append(value[number_of_features])
        X = np.ndarray(shape=(5,number_of_features), buffer = np.array(feature))
        y = np.array(status)

        self.knn = kn
        self.knn.partial_fit(X, y)

        n_samples = size
        corrects = right

        while (True):
            data = Stream_Classification_data.get_data(sensor_id, 1)
            X = np.ndarray(shape=(1, number_of_features), buffer=np.array(data[0][:number_of_features]))
            y = np.array([data[0][number_of_features]])
            my_pred = self.knn.predict(X)
            if y[0] == my_pred[0]:
                corrects += 1
            self.knn = self.knn.partial_fit(X, y)
            n_samples += 1
            time.sleep(30)
            if time.time()-start_time > time_to_run:
                break

        print('{} samples analyzed.'.format(n_samples))
        print('{} correct.'.format(corrects))
        print("KNN's performance: {}".format(corrects / n_samples))
        self.data_size = n_samples
        self.correct_predict = corrects
        self.accuracy = corrects/n_samples

        #sklearn2pmml(pipeline, "PMML/knn.pmml", with_repr = True)
