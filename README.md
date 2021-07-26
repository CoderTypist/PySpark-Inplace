# PySpark-Inplace

### Description
Apply transformation to PySpark DataFrames in place.

### Motivation
When you apply a transformation on a column, PySpark will duplicate the column and require you to provide the name for the column. For example, if you have a feature named "Department" and you want to use StringIndexer and OneHotEncoder, you will end up with three columns named "Department", "Department\_Indexed" and "Department\_Encoded".

This means you need to go through the hassle of giving columns new names and then referencing them by their new names. This quickly becomes tiresome. By using Inplace, you can simply create a list of all your features and reference that list for everything. 

# Documentation

## InplaceVariableCols
_class InplaceVariableCols(ABC):_

An abstract class that contains the implementation for a transformer for whom either 'inputCol' or 'inputCols' are valid arguments. 

|extends|description|
|---|---|
|ABC|Abstract class|

## InplaceVariableCols.\_\_init\_\_()
_def \_\_init\_\_(self, inputCol=None, inputCols=None):_

Constructor

|param|description|
|---|---|
|self||
|inputCol=None|Column to transform|
|inputCols=None|Columns to transform|

__returns:__ _None_
## InplaceVariableCols.init\_processor()
_def init\_processor(self):_

Abstract method in which subclasses must initialize the transformer to use.

|param|description|
|---|---|
|self||

__returns:__ _None_
## InplaceVariableCols.fit()
_def fit(self, df: pyspark.sql.dataframe.DataFrame) -> None:_

Fits the transformer to the data.

|param|description|
|---|---|
|self||
|df: pyspark.sql.dataframe.DataFrame|Fit the transformer using this data.|

__returns:__ _None_
## InplaceVariableCols.transform()
_def transform(self, df: pyspark.sql.dataframe.DataFrame) -> pyspark.sql.dataframe.DataFrame:_

Transform the incoming DataFrame

|param|description|
|---|---|
|self||
|df: pyspark.sql.dataframe.DataFrame|Data to transform|

__returns:__ _pyspark.sql.dataframe.DataFrame_:&nbsp; Transformed data
## InplaceVariableCols.fit\_transform()
_def fit\_transform(self, df\_fit, df\_transform=None) -> pyspark.sql.dataframe.DataFrame:_

Fit and transform the data. Fit and transform using the same DataFrame if df\_transform is not specified.

|param|description|
|---|---|
|self||
|df\_fit|Fit the transformer using this data.|
|df\_transform=None|Transform the following data. df\_fit is used by default.|

__returns:__ _pyspark.sql.dataframe.DataFrame_:&nbsp; Transformed data.
## InplaceStringIndexer
_class InplaceStringIndexer(InplaceVariableCols):_

Does the same thing as StringIndexer, but inplace.

|extends|description|
|---|---|
|InplaceVariableCols|Allows for the arguments 'inputCol' or 'inputCols'|

## InplaceStringIndexer.init\_processor()
_def init\_processor(self) -> StringIndexer:_

Initializes the StringIndexer.

|param|description|
|---|---|
|self||

__returns:__ _StringIndexer_:&nbsp; new StringIndexer
## InplaceOneHotEncoder
_class InplaceOneHotEncoder(InplaceVariableCols):_

Does the same thing as OneHotEncoder, but inplace.

|extends|description|
|---|---|
|InplaceVariableCols|Allows for the arguments 'inputCol' or 'inputCols'|

## InplaceOneHotEncoder.init\_processor()
_def init\_processor(self) -> OneHotEncoder:_

Initializes the OneHotEncoder.

|param|description|
|---|---|
|self||

__returns:__ _OneHotEncoder_:&nbsp; new OneHotEncoder
## InplaceVectorAssembler
_class InplaceVectorAssembler:_

XXX

## InplaceVectorAssembler.\_\_init\_\_()
_def \_\_init\_\_(self, inputCols, outputCol='Features'):_

Constructor

|param|description|
|---|---|
|self||
|inputCols|Columns to merge.|
|outputCol='Features'|Name of the output column.|

__returns:__ _None_
## InplaceVectorAssembler.transform()
_def transform(self, df) -> pyspark.sql.dataframe.DataFrame:_

Combine the inputCols into a single feature column.

|param|description|
|---|---|
|self||
|df|Merge the columns of this DataFrame.|

__returns:__ _pyspark.sql.dataframe.DataFrame_:&nbsp; DataFrame with feature column.
