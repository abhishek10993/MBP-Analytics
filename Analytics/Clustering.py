import findspark
findspark.init()

from pyspark.ml import Pipeline
from pyspark2pmml import PMMLBuilder
from pyspark.sql import SparkSession
from Data_Handlers import Data_Generator2
from pyspark.ml.clustering import KMeans
from pyspark import SparkContext
from pyspark.ml.feature import RFormula, VectorAssembler
from pyspark.sql import SQLContext
from pyspark.ml.evaluation import ClusteringEvaluator
import time

class Clustering:

    data_size = None
    centers = None
    silhouette = None
    exe_time = None
    type = 'Clustering'

    def __init__(self):
        pass

    def perform_clustering(self, sensor_id):
        start_time = time.time()
        sc= SparkContext()
        sqlContext = SQLContext(sc)
        spark = SparkSession.builder.appName("PySpark Clustering").config("spark.some.config.option", "some-value").getOrCreate()
        data = Data_Generator2.get_data()
        self.data_size = len(data.index)
        print(self.data_size)
        dataset = spark.createDataFrame(data)
        kmeans = KMeans().setK(2).setSeed(1)
        formula = RFormula(formula="Value ~ feature + Value")
        pipeline = Pipeline(stages=[formula, kmeans])
        model = pipeline.fit(dataset)

        vectorAssembler = VectorAssembler(inputCols=['feature', 'Value'], outputCol='features')
        feature_df = vectorAssembler.transform(dataset)
        predictions = model.stages[-1].transform(feature_df)
        evaluator = ClusteringEvaluator()
        self.silhouette = str(evaluator.evaluate(predictions))
        print("Silhouette with squared euclidean distance = " + self.silhouette)
        self.centers = model.stages[-1].clusterCenters()

        pmmlBuilder = PMMLBuilder(sc, dataset, model).putOption(kmeans, "compact", True)
        pmmlBuilder.buildFile("PMML/Cluster.pmml")
        self.exe_time = time.time() - start_time
        print('exe time in seconds: ', self.exe_time)
