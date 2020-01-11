import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler

from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from Data_Handlers import Data_Generator2
import pandas as pd


def perform_clustering():
    sc= SparkContext()
    sqlContext = SQLContext(sc)
    spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()

    # Loads data.
    #dataset = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load("/home/abhishek/data.csv")
    #print(dataset)
    data = Data_Generator2.get_data()
    dataset = sqlContext.createDataFrame(data)

    vectorAssembler = VectorAssembler(inputCols = ['X', 'Y'], outputCol = 'features')
    vhouse_df = vectorAssembler.transform(dataset)
    vhouse_df = vhouse_df.select(['features'])
    vhouse_df.show(3)
    # Trains a k-means model.
    kmeans = KMeans().setK(4).setSeed(1)
    model = kmeans.fit(vhouse_df)

    # Make predictions
    predictions = model.transform(vhouse_df)

    # Evaluate clustering by computing Silhouette score
    evaluator = ClusteringEvaluator()

    silhouette = evaluator.evaluate(predictions)
    print("Silhouette with squared euclidean distance = " + str(silhouette))

    # Shows the result.
    centers = model.clusterCenters()
    #ax.scatter(centers[0], centers[1], centers[2])
    print("Cluster Centers: ", centers)


perform_clustering()