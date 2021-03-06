import findspark
findspark.init()

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import RFormula, VectorAssembler, StringIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark2pmml import PMMLBuilder
import pandas as pd
from time import gmtime, strftime, time
from Data_Handlers import Dataframe_former

class Classification:

    test_error = None
    exe_time = None
    data_size = None
    type = "Classification"
    time_created = None
    description = None
    features = None

    def __init__(self):
        pass

    def perform_classification(self, sensor_id, model_name, model_description):
       start_time = time()
       self.description = model_description
       self.time_created = strftime("%Y-%m-%d %H:%M:%S", gmtime())
       sc = SparkContext()
       spark = SparkSession.builder.appName("Classification").config("spark.some.config.option","some-value").getOrCreate()
       try:
           data= Dataframe_former.download_data(sensor_id)
           df = spark.createDataFrame(data)
           (trainingData, testData) = df.randomSplit([0.7, 0.3])
           self.data_size = len(data.index)
           columns = list(data.columns.values)
           value = str(columns[len(columns)-1])
           self.features = columns[:len(columns) - 1]
           formula = RFormula(formula=value + " ~ .")
           classifier = DecisionTreeClassifier()
           pipeline = Pipeline(stages=[formula, classifier])
           pipelineModel = pipeline.fit(trainingData)
           vectorAssembler = VectorAssembler(inputCols = self.features,
                                             outputCol='features')
           vhouse_df = vectorAssembler.transform(testData)
           test = vhouse_df
           predictions = pipelineModel.stages[-1].transform(test)
           indexer = StringIndexer(inputCol=value, outputCol="categoryIndex")
           indexed = indexer.fit(df).transform(predictions)
           indexed.show(20)
           evaluator = MulticlassClassificationEvaluator(
               labelCol="categoryIndex", predictionCol="prediction", metricName="accuracy")
           accuracy = evaluator.evaluate(indexed)
           print("Test Error = %g " % (1.0 - accuracy))
           self.test_error = 1.0 - accuracy

           pmmlBuilder = PMMLBuilder(sc, df, pipelineModel).putOption(classifier, "compact", True)
           filename = "Analytics/PMML/" + model_name + ".pmml"
           pmmlBuilder.buildFile(filename)

           self.exe_time = time() - start_time
           print('exe time in seconds: ', self.exe_time)
           sc.stop()
       except:
           sc.stop()



