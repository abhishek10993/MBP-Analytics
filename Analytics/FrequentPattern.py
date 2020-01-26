import findspark
findspark.init()

from pyspark.sql.functions import split
from pyspark.ml.fpm import FPGrowth
from pyspark.sql import SparkSession
from Data_Handlers import Data_Generator3

class FrequentPattern:

    fpm = None

    def __init__(self):
        pass

    def find_fp(self):

        spark = SparkSession.builder.appName("Frequent Pattern").config("spark.some.config.option","some-value").getOrCreate()
        dataset = Data_Generator3.get_data()
        print(dataset)
        data = spark.read.text("../Data_Handlers/"+ dataset).select(split("value", "\s+").alias("items"))
        #data = spark.createDataFrame(dataset)
        data.show(truncate=True)
        fp = FPGrowth(minSupport=0.2, minConfidence=0.4)
        self.fpm = fp.fit(data)
        self.fpm.freqItemsets.sort("freq", ascending=False).show()
        self.fpm.associationRules.show()

        #pmmlBuilder = PMMLBuilder(sc, data, fpm).putOption(fp, "compact", True)
        #pmmlBuilder.buildFile("PMML/FP.pmml")
