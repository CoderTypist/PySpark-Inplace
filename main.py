from inplace import InplaceOneHotEncoder
from inplace import InplaceStringIndexer
from inplace import InplaceVectorAssembler
import pyspark
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession

from pyspark.ml.feature import IndexToString

def main():
    
    spark = SparkSession.builder.appName('Inplace_Example').getOrCreate()
    
    print('Read in csv')
    df_data = spark.read.csv('employees.csv', header=True, inferSchema=True)
    df_data.show()
    
    categorical = ['Sex', 'Department']
    features = ['Age', 'Sex', 'Department']
    
    print('Convert categorical variables into numbers')
    indexer = InplaceStringIndexer(inputCols=categorical)
    df_indexed = indexer.fit_transform(df_data)
    df_indexed.show()
    
    print('One-hot encode categorical variables')
    encoder = InplaceOneHotEncoder(inputCols=categorical)
    df_encoded = encoder.fit_transform(df_indexed)
    df_encoded.show()

    print('Group independent features together')
    assembler = InplaceVectorAssembler(inputCols=features)
    df_assembled = assembler.transform(df_encoded)
    df_assembled.show()
    
    print('Select data for model training and testing')
    df_dataset = df_assembled.select('Features', 'Salary')
    df_dataset.show()
    
    print('Train models and make predictions')
    X, y = df_dataset.randomSplit([0.80, 0.20])
    model = LinearRegression(featuresCol='Features', labelCol='Salary')
    model = model.fit(X)
    pred = model.evaluate(y)
    df_pred = pred.predictions
    df_pred.show()
    
    # This only works because each employee has a unique set of features
    # This is done merely for demonstration purposes
    print('Compare predictions to original values')
    df_join = df_pred.join(df_assembled.select('Name', 'Features'), 'Features')
    df_join = df_join.join(df_data.select('Name', 'Sex', 'Department'), 'Name')
    df_join.show()

if __name__ == '__main__':
    main()
