import numpy as np
from time import gmtime, strftime, time

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
        X = np.array([[1, 2], [1, 4], [1, 0],
                      [4, 2], [4, 0], [4, 4],
                      [4, 5], [0, 1], [2, 2],
                      [3, 2], [5, 5], [1, -1]])
        print(X)

        self.kmeans = km
        self.data_size = size
        #print(X[0:6,:])
        #print(X[6:12,:])
        for i in range(8):
            self.kmeans = self.kmeans.partial_fit(X[i:i+4,:])
            #print(self.kmeans.cluster_centers_,'\n')
            self.data_size += 1

        print(self.kmeans.cluster_centers_)
        #print(kmeans.predict([[0, 0], [4, 4]]))

        #pipeline = PMMLPipeline([("cluster", kmeans)])
        #sklearn2pmml(pipeline, "PMML/knn.pmml", with_repr = True)