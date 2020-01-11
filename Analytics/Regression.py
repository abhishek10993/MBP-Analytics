import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from Data_Handlers import Data_Generator
import numpy as np
import pandas as pd

def perform_regression():
#def perform_regression(sensor_id):
    sc = SparkContext()
    sqlContext = SQLContext(sc)
    #data = data_downloader(sensor_id)
    data = Data_Generator.get_data()
    df = sqlContext.createDataFrame(data)
    #house_df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('boston.csv')
    vectorAssembler = VectorAssembler(
        inputCols=['X','Y'],
        outputCol='features')
    vhouse_df = vectorAssembler.transform(df)
    vhouse_df = vhouse_df.select(['features', 'Value'])
    splits = vhouse_df.randomSplit([0.7, 0.3])
    train_df = splits[0]
    test_df = splits[1]

    lr = LinearRegression(featuresCol='features', labelCol='Value', maxIter=10, regParam=0.3, elasticNetParam=0.8)
    lr_model = lr.fit(train_df)
    print("Coefficients: " + str(lr_model.coefficients))
    print("Intercept: " + str(lr_model.intercept))

    trainingSummary = lr_model.summary
    print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
    print("r2: %f" % trainingSummary.r2)

    lr_predictions = lr_model.transform(test_df)
    lr_predictions.select("prediction", "Value", "features").show(20)

    lr_evaluator = RegressionEvaluator(predictionCol="prediction", \
                                       labelCol="Value", metricName="r2")
    print("R Squared (R2) on test data = %g" % lr_evaluator.evaluate(lr_predictions))

    test_result = lr_model.evaluate(test_df)
    print("Root Mean Squared Error (RMSE) on test data = %g" % test_result.rootMeanSquaredError)

    print("numIterations: %d" % trainingSummary.totalIterations)
    print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
    trainingSummary.residuals.show()

    predictions = lr_model.transform(test_df)
    predictions.select("prediction", "Value", "features").show()


perform_regression()