import numpy as np
from time import gmtime, strftime, time
from Data_Handlers import Stream_kmeans_data
import configparser

class KMeans_stream_clustering:
    data_size = None
    correct_predict = None
    kmeans = None
    type = 'Stream KMeans Clustering'
    time_created = None
    description = None

    def __init__(self):
        pass

    def create_kmeans_stream_model(self, km, size, sensor_id, model_description):
        self.time_created = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.description = model_description
        X = Stream_kmeans_data.get_data(sensor_id,4)
        self.kmeans = km
        self.data_size = size
        #print(X[0:6,:])
        #print(X[6:12,:])
        self.kmeans = self.kmeans.partial_fit(X)
        start_time = time.time()
        config = configparser.RawConfigParser()
        config.read('../resources/misc.properties')
        time_to_run = int(config.get('time', 'streamsave')) * 60
        while (True):
            X = Stream_kmeans_data.get_data('5e861c0e016d04a47cf155cf', 2)
            self.kmeans = self.kmeans.partial_fit(X)
            print(X)
            self.data_size += 1
            time.sleep(60)
            if time.time() - start_time > time_to_run:
                break

        print(self.kmeans.cluster_centers_)
        #print(kmeans.predict([[0, 0], [4, 4]]))

        #pipeline = PMMLPipeline([("cluster", kmeans)])
        #sklearn2pmml(pipeline, "PMML/knn.pmml", with_repr = True)