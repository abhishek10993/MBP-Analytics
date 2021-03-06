from .Regression import Regression
from .FrequentPattern import FrequentPattern
from .Clustering import Clustering
from .Classification import Classification
from .KNN_stream import KNN_stream
from .KMeans_stream_clustering import KMeans_stream_clustering
from .Hoeffdingtree_stream import Hoeffdingtree_stream
import pickle
from sklearn.cluster import MiniBatchKMeans
from skmultiflow.lazy import KNN
from skmultiflow.trees import HoeffdingTree


def create_regression_model(model_name, sensor_id, model_description):
    regression = Regression()
    regression.perform_regression(sensor_id, model_name, model_description)

    with open('Analytics/Pickle_files/'+model_name+'.pickle', 'wb') as f:
        pickle.dump(regression, f)

def create_fp_model(model_name, sensor_id, model_description):
    fp = FrequentPattern()
    fp.find_fp(sensor_id, model_description)

    with open('Analytics/Pickle_files/'+model_name+'.pickle', 'wb') as f:
        pickle.dump(fp, f)


def create_clustering_model(model_name, sensor_id, model_description):
    cluster = Clustering()
    cluster.perform_clustering(sensor_id, model_name, model_description)

    with open('Analytics/Pickle_files/'+model_name+'.pickle', 'wb') as f:
        pickle.dump(cluster, f)

def create_classification_model(model_name, sensor_id, model_description):
    classification = Classification()
    classification.perform_classification(sensor_id, model_name, model_description)

    with open('Analytics/Pickle_files/'+model_name+'.pickle', 'wb') as f:
        pickle.dump(classification, f)

def create_knn_stream(model_name, sensor_id, snapshots, model_description):
    knn = KNN()
    size = 0
    correct = 0
    snapshot = 1
    while snapshot<=snapshots:
        #print("\n\niteration: ",snapshots)
        obj = KNN_stream()
        obj.create_knn_model(knn, size, correct, sensor_id, model_description)
        print(obj.data_size, '***data processed***\n\n')
        filename = "Analytics/Pickle_files/"+model_name+ "_v" + str(snapshot)+".pickle"
        snapshot+=1
        size = obj.data_size
        correct = obj.correct_predict
        knn = obj.knn
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)

def create_kmeans_stream(model_name, sensor_id, snapshots, model_description):
    kmeans = MiniBatchKMeans(n_clusters=4, random_state=0, batch_size=4)
    size = 0
    snapshot = 1
    while snapshot<=snapshots:
        #print("\n\niteration: ",snapshots)
        obj = KMeans_stream_clustering()
        obj.create_kmeans_stream_model(kmeans, size, sensor_id, model_description)
        print(obj.data_size, '***data processed***\n\n')
        print(obj.kmeans.cluster_centers_)
        filename = "Analytics/Pickle_files/"+model_name+ "_v" + str(snapshot)+".pickle"
        snapshot+=1
        size = obj.data_size
        kmeans = obj.kmeans
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)

def create_hoeffdingtree_stream(model_name, sensor_id, snapshots, model_description):
    tree = HoeffdingTree()
    size = 0
    correct = 0
    snapshot = 1
    while snapshot<=snapshots:
        #print("\n\niteration: ",snapshots)
        obj = Hoeffdingtree_stream()
        obj.create_hoeffdingtree_model(tree, size, correct, sensor_id, model_description)
        print(obj.accuracy)
        print(obj.data_size, '***data processed***\n\n')
        filename = "Analytics/Pickle_files/"+model_name+ "_v" + str(snapshot)+".pickle"
        snapshot+=1
        size = obj.data_size
        correct = obj.correct_predict
        tree = obj.hoeffding_tree
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)

