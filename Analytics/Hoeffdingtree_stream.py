import configparser
from time import gmtime, strftime
from Data_Handlers import Stream_Classification_data
import numpy as np
import time

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
            start_time = time.time()
            config = configparser.RawConfigParser()
            config.read('../resources/misc.properties')
            time_to_run = int(config.get('time', 'streamsave')) * 60
            data = Stream_Classification_data.get_data(sensor_id,5)
            feature = []
            status = []
            number_of_features = len(data[0])
            # print(data)
            for value in data:
                feature.append(value[:number_of_features])
                status.append(value[number_of_features])
            #print(feature)
            #print(status)
            X = np.ndarray(shape=(5, number_of_features), buffer=np.array(feature))
            y = np.array(status)
            #print(X, "**")
            #print(y, "**")
            self.hoeffding_tree = tree
            self.hoeffding_tree.partial_fit(X,y)

            corrects = correct
            n_samples = size

            while (True):
                data = Stream_Classification_data.get_data(1)
                X = np.ndarray(shape=(1, number_of_features), buffer=np.array(data[0][:number_of_features]))
                #print(X, "**")
                y = np.array([data[0][number_of_features]])
                #print(y, "**")
                prediction = self.hoeffding_tree.predict(X)  # predict Y using the tree
                if y == prediction:                # check the prediction
                    corrects +=1
                self.hoeffding_tree.partial_fit(X, y)
                n_samples += 1
                time.sleep(30)
                if time.time()-start_time > time_to_run:
                    break

            self.data_size = n_samples
            self.correct_predict = corrects
            self.accuracy = corrects / n_samples