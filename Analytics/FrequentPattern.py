import findspark
findspark.init()

from pyspark.sql.functions import split
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.fpm import FPGrowth
from pyspark.ml.regression import LinearRegression, SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from Data_Handlers import Data_Generator3


def find_fp():
    spark = SparkSession.builder.appName("Frequent Pattern").config("spark.some.config.option","some-value").getOrCreate()
    data = spark.read.text("../Data_Handlers/data.txt").select(split("value", "\s+").alias("items"))
    data.show(truncate=True)
    fp = FPGrowth(minSupport=0.2, minConfidence=0.4)
    fpm = fp.fit(data)
    fpm.freqItemsets.show(5)
    fpm.associationRules.show(5)


find_fp()