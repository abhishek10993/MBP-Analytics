import findspark
from pyspark import SparkContext, SQLContext
from pyspark.sql import SparkSession

findspark.init()

from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import RFormula
from pyspark2pmml import PMMLBuilder
import pandas as pd
from pypmml import Model

def perform_classification():
    sc = SparkContext()
    sqlContext = SQLContext(sc)
    spark = SparkSession.builder.appName("Classification").config("spark.some.config.option","some-value").getOrCreate()
    data= pd.read_csv("/home/abhishek/Downloads/Iris.csv")
    df = spark.createDataFrame(data)
    formula = RFormula(formula="Species ~ .")
    classifier = DecisionTreeClassifier()
    pipeline = Pipeline(stages=[formula, classifier])
    pipelineModel = pipeline.fit(df)

    pmmlBuilder = PMMLBuilder(sc, df, pipelineModel).putOption(classifier, "compact", True)
    pmmlBuilder.buildFile("PMML/DecisionTreeIris.pmml")

    model = Model.fromFile("PMML/DecisionTreeIris.pmml")
    result = model.predict({'sepal_length': 2.1, 'sepal_width': 5.5, 'petal_length': 2.4, 'petal_width': 1.0})
    print(result)




perform_classification()