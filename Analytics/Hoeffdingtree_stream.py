import configparser
import requests
import time
from Data_Handlers import Data_Handler_knn
import numpy as np
from skmultiflow.trees import HoeffdingTree

class Hoeffdingtree_stream:

    def __init__(self):
        pass

    def create_model(self):
            data = Data_Handler_knn.get_data(5)
            feature = []
            status = []
            # print(data)
            for value in data:
                feature.append(value[:3])
                status.append(value[3])
            print(feature)
            print(status)
            X = np.ndarray(shape=(5, 3), buffer=np.array(feature))
            y = np.array(status)
            print(X, "**")
            print(y, "**")
            tree = HoeffdingTree()
            tree.partial_fit(X,y)

            correctness_dist = []
            n_samples = 0

            while (True):
                data = Data_Handler_knn.get_data(1)
                X = np.ndarray(shape=(1, 3), buffer=np.array(data[0][:3]))
                print(X, "**")
                y = np.array([data[0][3]])
                print(y, "**")
                prediction = tree.predict(X)  # predict Y using the tree
                if y == prediction:                # check the prediction
                    correctness_dist.append(1)
                else:
                    correctness_dist.append(0)
                tree.partial_fit(X, y)
                n_samples += 1
                if n_samples == 20:
                    break

            print('\n\n')
            print(correctness_dist)
            print(n_samples)