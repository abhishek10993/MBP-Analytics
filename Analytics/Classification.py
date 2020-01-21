import findspark
findspark.init()

from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from Data_Handlers import Data_Generator2
from pyspark.sql import Row
from pyspark.ml.linalg import Vectors

# Load training data
sc = SparkContext()
sqlContext = SQLContext(sc)
spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option",
                                                                              "some-value").getOrCreate()
data = Data_Generator2.get_data()
dataset = sqlContext.createDataFrame(data)

vectorAssembler = VectorAssembler(inputCols=['X', 'Y'], outputCol='features')
vhouse_df = vectorAssembler.transform(dataset)
vhouse_df = vhouse_df.select(['features'])
vhouse_df.show(3)

splits = vhouse_df.randomSplit([0.6, 0.4], 1234)
train = splits[0]
test = splits[1]

nb = NaiveBayes(smoothing=1.0, modelType="multinomial")

model = nb.fit(train)

# select example rows to display.
predictions = model.transform(test)
predictions.show()

# compute accuracy on the test set
evaluator = MulticlassClassificationEvaluator(labelCol="features", predictionCol="prediction",
                                              metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test set accuracy = " + str(accuracy))