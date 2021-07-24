# PySpark-Inplace

### Description
Apply transformation to PySpark DataFrames in place.

### Motivation
When you apply a transformation on a column, PySpark will duplicate the column and require you to provide the name for the column. For example, if you have a feature named "Department" and you want to use StringIndexer and OneHotEncoder, you will end up with three columns named "Department", "Department\_Indexed" and "Department\_Encoded".

This means you need to go through the hassle of giving columns new names and then referencing them by their new names. This quickly becomes tiresome. By using Inplace, you can simply create a list of all your features and reference that list for everything. 
