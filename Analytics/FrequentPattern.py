import findspark
findspark.init()

from pyspark.sql.functions import split
from pyspark.ml.fpm import FPGrowth
from pyspark.sql import SparkSession
from Data_Handlers import Data_Generator3
import time

class FrequentPattern:

    frequent_patterns = None
    exe_time = None
    assocaition_rules = None

    def __init__(self):
        pass

    def find_fp(self):
        start_time = time.time()
        spark = SparkSession.builder.appName("Frequent Pattern").config("spark.some.config.option","some-value").getOrCreate()
        dataset = Data_Generator3.get_data()
        print(dataset)
        data = spark.read.text("../Data_Handlers/"+ dataset).select(split("value", "\s+").alias("items"))
        #data = spark.createDataFrame(dataset)
        data.show(truncate=True)
        fp = FPGrowth(minSupport=0.2, minConfidence=0.4)
        fpm = fp.fit(data)
        self.frequent_patterns = fpm.freqItemsets.sort("freq", ascending=False).show()
        self.assocaition_rules = fpm.associationRules.show()
        self.exe_time = time.time() - start_time
        print('exe time in seconds: ', self.exe_time)

        #pmmlBuilder = PMMLBuilder(sc, data, fpm).putOption(fp, "compact", True)
        #pmmlBuilder.buildFile("PMML/FP.pmml")
