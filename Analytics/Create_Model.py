from Regression import Regression
from FrequentPattern import FrequentPattern
from Clustering import Clustering
from Classification import Classification
from KNN_stream import KNN_stream
from KMeans_stream_clustering import KMeans_stream_clustering
from Hoeffdingtree_stream import Hoeffdingtree_stream
import pickle
from sklearn.cluster import MiniBatchKMeans
from skmultiflow.lazy import KNN
from skmultiflow.trees import HoeffdingTree


def create_regression_model():
    regression = Regression()
    regression.perform_regression()

    print(regression.rmse)
    print(regression.coefficients)
    print(regression.intercept)

    with open('Pickle_files/regression.pickle', 'wb') as f:
        pickle.dump(regression, f)

    print('loading file')
    file = open('Pickle_files/regression.pickle', 'rb')
    new = pickle.load(file)

    print(new.rmse)
    print(new.intercept)

def create_fp_model():
    fp = FrequentPattern()
    fp.find_fp()

    with open('Pickle_files/frequentpattern.pickle', 'wb') as f:
        pickle.dump(fp, f)


def create_clustering_model():
    cluster = Clustering()
    cluster.perform_clustering()

    with open('Pickle_files/Clustering.pickle', 'wb') as f:
        pickle.dump(cluster, f)

def create_classification_model():
    classification = Classification()
    classification.perform_classification()

    with open('Pickle_files/classification.pickle', 'wb') as f:
        pickle.dump(classification, f)

def create_knn_stream():
    knn = KNN()
    size = 0
    correct = 0
    snapshots = 1
    while snapshots<=10:
        print("\n\niteration: ",snapshots)
        obj = KNN_stream()
        obj.create_knn_model(knn, size, correct)
        print(obj.data_size, '***data processed***\n\n')
        filename = "Pickle_files/knn_"+str(snapshots)+".pickle"
        snapshots+=1
        size = obj.data_size
        correct = obj.correct_predict
        knn = obj.knn
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)

def create_kmeans_stream():
    kmeans = MiniBatchKMeans(n_clusters=2, random_state=0, batch_size=6)
    size = 0
    #correct = 0
    snapshots = 1
    while snapshots<=10:
        print("\n\niteration: ",snapshots)
        obj = KMeans_stream_clustering()
        obj.create_kmeans_stream_model(kmeans, size)
        print(obj.data_size, '***data processed***\n\n')
        print(obj.kmeans.cluster_centers_)
        filename = "Pickle_files/kmeans_"+str(snapshots)+".pickle"
        snapshots+=1
        size = obj.data_size
        kmeans = obj.kmeans
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)

def create_hoeffdingtree_stream():
    tree = HoeffdingTree()
    size = 0
    correct = 0
    snapshots = 1
    while snapshots<=10:
        print("\n\niteration: ",snapshots)
        obj = Hoeffdingtree_stream()
        obj.create_hoeffdingtree_model(tree, size, correct)
        print(obj.accuracy)
        print(obj.data_size, '***data processed***\n\n')
        filename = "Pickle_files/hoeff_tree_"+str(snapshots)+".pickle"
        snapshots+=1
        size = obj.data_size
        correct = obj.correct_predict
        tree = obj.hoeffding_tree
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)


create_hoeffdingtree_stream()
