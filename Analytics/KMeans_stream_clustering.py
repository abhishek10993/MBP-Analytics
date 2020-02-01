from sklearn.cluster import MiniBatchKMeans
import numpy as np

class KMeans_stream_clustering:
    rmse = None
    data_size = None
    correct_predict = None
    kmeans = None
    type = 'Stream K-Means Clustering'

    def __init__(self):
        pass

    def create_kmeans_stream_model(self, km, size, sensor_id):

        X = np.array([[1, 2], [1, 4], [1, 0],
                      [4, 2], [4, 0], [4, 4],
                      [4, 5], [0, 1], [2, 2],
                      [3, 2], [5, 5], [1, -1]])
        print(X)

        self.kmeans = km
        self.data_size = size
        #print(X[0:6,:])
        #print(X[6:12,:])
        for i in range(11):
            self.kmeans = self.kmeans.partial_fit(X[i:i+2,:])
            #print(self.kmeans.cluster_centers_,'\n')
            self.data_size += 1
        #kmeans = kmeans.partial_fit(X[6:12,:])
        #print(kmeans.cluster_centers_)
        #print(kmeans.predict([[0, 0], [4, 4]]))

        #print("*******************************************\n\n")
        #kmeans = MiniBatchKMeans(n_clusters=2,random_state=0, batch_size=6, max_iter=10).fit(X)

        #print(kmeans.cluster_centers_)
        #print(kmeans.predict([[0, 0], [4, 4]]))

        #pipeline = PMMLPipeline([("cluster", kmeans)])
        #sklearn2pmml(pipeline, "PMML/knn.pmml", with_repr = True)