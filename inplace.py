from abc import ABC, abstractmethod
import pyspark
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler


class InplaceVariableCols(ABC):
    
    def __init__(self, inputCol=None, inputCols=None):
        
        # must pick one or the other
        if inputCol and inputCols:
            raise Exception('Cannot specify inputCol and inputCols')
        
        # one input column
        elif inputCol:
            self.single = True
            self.inputCol = inputCol
            self.outputCol = self.inputCol + '_processed'
        
        # multiple input columns
        elif inputCols:
            self.single = False
            self.inputCols = inputCols
            self.outputCols = [c+'_encoded' for c in self.inputCols]
            
        else:
            raise Exception('Must specify inputCol or inputCols')
            
        self.isfitted = False
        self.processor = self.init_processor()
        
    @abstractmethod
    def init_processor(self):
        pass
        
    def fit(self, df: pyspark.sql.dataframe.DataFrame) -> None:
        self.processor = self.processor.fit(df)
        self.isfitted = True
    
    def transform(self, df: pyspark.sql.dataframe.DataFrame) -> pyspark.sql.dataframe.DataFrame:
        
        if not self.isfitted:
            raise Exception('Must fit before transforming')
            
        df_new = self.processor.transform(df)
        
        if self.single:
            df_new = df_new.drop(self.inputCol)
            df_new = df_new.withColumnRenamed(self.outputCol, self.inputCol)
            
        else:
            for in_col, out_col in zip(self.inputCols, self.outputCols):
                df_new = df_new.drop(in_col)
                df_new = df_new.withColumnRenamed(out_col, in_col)
                
        return df_new
                
    def fit_transform(self, df_fit, df_transform) -> pyspark.sql.dataframe.DataFrame:
        
        if self.isfitted:
            return self.transform(df_transform)
        
        else:
            self.fit(df_fit)
            
            if df_transform:
                return self.transform(df_transform)
            else:
                return self.transform(df_fit)
        

class InplaceStringIndexer(InplaceVariableCols):
    
    def init_processor(self) -> StringIndexer:
        
        if self.single:
            return StringIndexer(inputCol=self.inputCol, outputCol=self.outputCol)
        else:
            return StringIndexer(inputCols=self.inputCols, outputCols=self.outputCols)
        
        
class InplaceOneHotEncoder(InplaceVariableCols):
    
    def init_processor(self) -> StringIndexer:
        
        if self.single:
            return OneHotEncoder(inputCol=self.inputCol, outputCol=self.outputCol)
        else:
            return OneHotEncoder(inputCols=self.inputCols, outputCols=self.outputCols)

class InplaceVectorAssembler:
    
    def __init__(self, inputCols, outputCol='Features'):
        
        self.inputCols = inputCols
        self.outputCol = outputCol
        self.assembler = VectorAssembler(inputCols = self.inputCols, outputCol = self.outputCol)
    
    def transform(self, df) -> pyspark.sql.dataframe.DataFrame:
        df_new = self.assembler.transform(df)
        
        for c in self.inputCols:
            df_new = df_new.drop(c)
            
        return df_new
