import findspark
findspark.init()

from pyspark.ml import Pipeline
from pyspark2pmml import PMMLBuilder
from pyspark.sql import SparkSession
from Data_Handlers import Data_Generator2
from pyspark.ml.clustering import KMeans
from pyspark import SparkContext
from pyspark.ml.feature import RFormula
from pyspark.sql import SQLContext
from pypmml import Model
from pypmml_spark import ScoreModel
import numpy as np
import pandas as pd


def perform_clustering():
    sc= SparkContext()
    sqlContext = SQLContext(sc)
    spark = SparkSession.builder.appName("PySpark Clustering").config("spark.some.config.option", "some-value").getOrCreate()
    data = Data_Generator2.get_data()
    dataset = spark.createDataFrame(data)
    kmeans = KMeans().setK(2).setSeed(1)
    formula = RFormula(formula="Value ~ feature + Value")
    pipeline = Pipeline(stages=[formula, kmeans])
    model = pipeline.fit(dataset)

    pmmlBuilder = PMMLBuilder(sc, dataset, model).putOption(kmeans, "compact", True)
    pmmlBuilder.buildFile("PMML/Cluster.pmml")


    #print(model.__getattribute__('Cluster'))
    #print(model.outputFields)
    #print(model.functionName)


perform_clustering()