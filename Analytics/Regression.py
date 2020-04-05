import findspark
findspark.init()

from pyspark.ml import Pipeline
from pyspark2pmml import PMMLBuilder
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler, RFormula
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from Data_Handlers import Dataframe_former
from time import gmtime, strftime, time

class Regression:
    rmse = None
    exe_time = None
    data_size = None
    coefficients = None
    intercept = None
    type = 'Regression'
    time_created = None
    description = None
    features = None

    def __init__(self):
        pass

    def perform_regression(self, sensor_id, model_name, model_description):
        self.time_created = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.description = model_description
        start_time = time()
        sc = SparkContext()
        sqlContext = SQLContext(sc)
        #data = data_downloader(sensor_id)
        try:
            data = Dataframe_former.download_data(sensor_id)
            self.data_size = len(data.index)
            columns = list(data.columns.values)
            value = str(columns[len(columns) - 1])
            self.features = columns[:len(columns) - 1]
            data= data.groupby(self.features, as_index=False).sum()
            print(data.columns)
            df = sqlContext.createDataFrame(data)
            df.show()

            formula = RFormula(formula=value + " ~ .")
            splits = df.randomSplit([0.7, 0.3])
            train_df = splits[0]
            test_df = splits[1]
            lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
            pipeline = Pipeline(stages=[formula, lr])
            lr_model = pipeline.fit(df)

            print("Coefficients: " + str(lr_model.stages[-1].coefficients))
            self.coefficients= str(lr_model.stages[-1].coefficients)
            print("Intercept: " + str(lr_model.stages[-1].intercept))
            self.intercept = str(lr_model.stages[-1].intercept)

            trainingSummary = lr_model.stages[-1].summary
            print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
            self.rmse = trainingSummary.rootMeanSquaredError
            print("r2: %f" % trainingSummary.r2)
            vectorAssembler = VectorAssembler(inputCols=self.features, outputCol='features')
            vhouse_df = vectorAssembler.transform(test_df)
            lr_predictions = lr_model.stages[-1].transform(vhouse_df)
            lr_predictions.select("prediction", value, "features").show()

            lr_evaluator = RegressionEvaluator(predictionCol="prediction", labelCol=value, metricName="r2")
            print("R Squared (R2) on test data = %g" % lr_evaluator.evaluate(lr_predictions))

            pmmlBuilder = PMMLBuilder(sc, train_df, lr_model).putOption(lr, "compact", True)
            filename = "Analytics/PMML/"+model_name+".pmml"
            pmmlBuilder.buildFile(filename)
            sc.stop()
            self.exe_time = time() - start_time
            print('exe time in seconds: ', self.exe_time)
        except:
            sc.stop()
