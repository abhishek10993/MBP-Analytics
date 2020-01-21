import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark2pmml import PMMLBuilder
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import HashingTF, Tokenizer
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
    #cluster = KMeans()
    kmeans = KMeans().setK(4).setSeed(1)
    tokenizer = Tokenizer(inputCol="X", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features_X")
    pipeline = Pipeline(stages=[tokenizer, hashingTF, kmeans])
    model = pipeline.fit(dataset)

    # Make predictions
    predictions = model.transform(vhouse_df)

    # Evaluate clustering by computing Silhouette score
    evaluator = ClusteringEvaluator()

    silhouette = evaluator.evaluate(predictions)
    print("Silhouette with squared euclidean distance = " + str(silhouette))

    #javaDf = _py2java(sc, dataset)
    #javaSchema = javaDf.schema.__call__()
    #javaPipelineModel = kmeans._to_java()
    #javaPmmlBuilderClass = sc._jvm.org.jpmml.sparkml.PMMLBuilder
    #javaPmmlBuilder = javaPmmlBuilderClass(javaSchema, javaPipelineModel)
    #javaPmmlBuilder.buildFile("Cluster.pmml")

    pmmlBuilder = PMMLBuilder(sc, dataset, pipeline).putOption(pipeline, "compact", True)
    pmmlBuilder.buildFile("Cluster.pmml")

    # Shows the result.
    centers = model.clusterCenters()
    #ax.scatter(centers[0], centers[1], centers[2])
    print("Cluster Centers: ", centers)


perform_clustering()