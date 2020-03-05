import configparser
import requests
from time import gmtime, strftime, time
from Data_Handlers import Data_Handler_knn
import numpy as np

class Hoeffdingtree_stream:

    accuracy = None
    data_size = None
    correct_predict = None
    hoeffding_tree = None
    type = 'Stream Hoeffding Tree Classifier'
    time_created = None
    description = None

    def __init__(self):
        pass

    def create_hoeffdingtree_model(self, tree, size, correct, sensor_id, model_description):
            self.time_created = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            self.description = model_description
            data = Data_Handler_knn.get_data(5)
            feature = []
            status = []
            # print(data)
            for value in data:
                feature.append(value[:3])
                status.append(value[3])
            #print(feature)
            #print(status)
            X = np.ndarray(shape=(5, 3), buffer=np.array(feature))
            y = np.array(status)
            #print(X, "**")
            #print(y, "**")
            self.hoeffding_tree = tree
            self.hoeffding_tree.partial_fit(X,y)

            corrects = correct
            n_samples = size
            datapoints = 0

            while (True):
                data = Data_Handler_knn.get_data(1)
                X = np.ndarray(shape=(1, 3), buffer=np.array(data[0][:3]))
                #print(X, "**")
                y = np.array([data[0][3]])
                #print(y, "**")
                prediction = self.hoeffding_tree.predict(X)  # predict Y using the tree
                if y == prediction:                # check the prediction
                    corrects +=1
                self.hoeffding_tree.partial_fit(X, y)
                n_samples += 1
                datapoints += 1
                if datapoints == 20:
                    break

            self.data_size = n_samples
            self.correct_predict = corrects
            self.accuracy = corrects / n_samples