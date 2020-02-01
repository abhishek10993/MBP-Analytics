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
import time

class Classification:

    test_error = None
    exe_time = None
    data_size = None
    type = "Classification"

    def __init__(self):
        pass

    def perform_classification(self, sensor_id):
       start_time = time.time()
       sc = SparkContext()
       spark = SparkSession.builder.appName("Classification").config("spark.some.config.option","some-value").getOrCreate()
       data= pd.read_csv("/home/abhishek/Downloads/Iris.csv")
       df = spark.createDataFrame(data)
       (trainingData, testData) = df.randomSplit([0.7, 0.3])
       self.data_size = len(data.index)
       formula = RFormula(formula="Species ~ .")
       classifier = DecisionTreeClassifier()
       pipeline = Pipeline(stages=[formula, classifier])
       pipelineModel = pipeline.fit(trainingData)
       vectorAssembler = VectorAssembler(inputCols=['Sepal_Length', 'Sepal_Width', 'Petal_Length', 'Petal_Width'],
                                         outputCol='features')
       vhouse_df = vectorAssembler.transform(testData)
       test = vhouse_df
       predictions = pipelineModel.stages[-1].transform(test)
       indexer = StringIndexer(inputCol="Species", outputCol="categoryIndex")
       indexed = indexer.fit(df).transform(predictions)
       indexed.show(20)
       evaluator = MulticlassClassificationEvaluator(
           labelCol="categoryIndex", predictionCol="prediction", metricName="accuracy")
       accuracy = evaluator.evaluate(indexed)
       print("Test Error = %g " % (1.0 - accuracy))
       self.test_error = 1.0 - accuracy

       pmmlBuilder = PMMLBuilder(sc, df, pipelineModel).putOption(classifier, "compact", True)
       pmmlBuilder.buildFile("PMML/DecisionTree.pmml")

       self.exe_time = time.time() - start_time
       print('exe time in seconds: ', self.exe_time)



