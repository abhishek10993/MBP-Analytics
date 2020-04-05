import findspark
findspark.init()

from pyspark.sql.functions import split
from pyspark.ml.fpm import FPGrowth
from pyspark.sql import SparkSession
from Data_Handlers import FP_data
from time import gmtime, strftime, time

class FrequentPattern:

    frequent_patterns = None
    exe_time = None
    assocaition_rules = None
    type = 'Frequent Pattern mining'
    time_created = None
    description = None
    data_size = None
    min_support = None
    min_confidence = None

    def __init__(self):
        pass

    def find_fp(self, sensor_id, model_description):
        start_time = time()
        self.description = model_description
        self.time_created = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        spark = SparkSession.builder.appName("Frequent Pattern").config("spark.some.config.option","some-value").getOrCreate()
        try:
            dataset = FP_data.get_data(sensor_id)
            self.data_size = 5000
            print(dataset)
            data = spark.read.text(dataset).select(split("value", "\s+").alias("items"))
            #data = spark.createDataFrame(dataset)
            data.show()
            print('got data\n\n')
            self.min_confidence = 0.2
            self.min_support = 0.05
            #fp = FPGrowth(minSupport=self.min_support, minConfidence=self.min_confidence)
            fp = FPGrowth(itemsCol="items", minSupport=0.5, minConfidence=0.5)
            fpm = fp.fit(data)
            print('fpm created\n\n')
            print(fpm.freqItemsets.sort("freq", ascending=False))
            print(fpm.associationRules)
            self.frequent_patterns = fpm.freqItemsets.sort("freq", ascending=False).toPandas()
            self.assocaition_rules = fpm.associationRules.toPandas()
            self.exe_time = time() - start_time
            print('exe time in seconds: ', self.exe_time)
            spark.stop()
        except:
            spark.stop()