import pickle
import numpy as np

def get_statistics(model_name):
    print('loading file')
    file = open('Pickle_files/knn3.pickle', 'rb')
    new = pickle.load(file)

    print(new.data_size)
    print(new.correct_predict)
    X = np.ndarray(shape=(1, 3), buffer=np.array([94, 5.0, 6.0]))
    print(new.knn.predict(X))

    print('loading file')
    file = open('Pickle_files/knn5.pickle', 'rb')
    new = pickle.load(file)

    print(new.data_size)
    print(new.correct_predict)
    print(new.knn.predict(X))
