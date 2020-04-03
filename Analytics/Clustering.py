import findspark
findspark.init()

from pyspark.ml import Pipeline
from pyspark2pmml import PMMLBuilder
from pyspark.sql import SparkSession
from Data_Handlers import Dataframe_former
from pyspark.ml.clustering import KMeans
from pyspark import SparkContext
from pyspark.ml.feature import RFormula, VectorAssembler
from pyspark.sql import SQLContext
from pyspark.ml.evaluation import ClusteringEvaluator
from time import gmtime, strftime, time

class Clustering:

    data_size = None
    centers = None
    silhouette = None
    exe_time = None
    type = 'Clustering'
    time_created = None
    description = None


    def __init__(self):
        pass

    def perform_clustering(self, sensor_id, model_name, model_description):
        start_time = time()
        self.description = model_description
        self.time_created = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        sc= SparkContext()
        sqlContext = SQLContext(sc)
        spark = SparkSession.builder.appName("PySpark Clustering").config("spark.some.config.option", "some-value").getOrCreate()
        data = Dataframe_former.get_data(sensor_id)
        self.data_size = len(data.index)
        print(self.data_size)
        dataset = spark.createDataFrame(data)
        kmeans = KMeans().setK(4).setSeed(1)
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
        filename = "Analytics/PMML/" + model_name + ".pmml"
        pmmlBuilder.buildFile(filename)
        self.exe_time = time() - start_time
        print('exe time in seconds: ', self.exe_time)
        sc.stop()
