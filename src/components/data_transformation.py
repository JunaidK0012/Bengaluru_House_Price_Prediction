import os 
import sys
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import get_columns,save_obj
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

@dataclass 
class DataTransformationConfig:
    """
    A data class that holds configuration information for the data transformation process.

    Attributes:
        preprocessor_obj_path (str): The path where the preprocessor object will be stored.
        data_path (str): The path where the cleaned data without outliers is located.
    """
    preprocessor_obj_path : str 
    data_path : str

class DataTransformation:
    """
    A class used for data transformation.

    Attributes:
        config (DataTransformationConfig): The configuration information for the data cleaning process.
    """

    def __init__(self,config:DataTransformationConfig):
        self.config = config

    def get_preprocessor_obj(self,cat_columns : list[str] ,num_columns : list[str]):
        """
        The function to get the preprocessor object.

        Parameters:
            cat_columns (list) : List of categorical columns.
            num_columns (list) : List of numerical columns.

        Returns:
            preprocessor_obj (ColumnTransformer) : The preprocessor object.
        """
        try:
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('encoder',OneHotEncoder(handle_unknown='ignore'))
                ]
            )

            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )

            preprocessor_obj = ColumnTransformer([
                ('num_pipeline',num_pipeline,num_columns),
                ('cat_pipeline',cat_pipeline,cat_columns)
            ],remainder='passthrough')

            

            return preprocessor_obj
            
        except Exception as e:
            logging.error(f"An error occurred while creating the preprocessor object: {e}")
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self):
        """
        The function to initiate the data transformation process.

        Returns:
            X_train, X_test, y_train, y_test (ndarray) : Transformed training and test sets.
           
        """
        logging.info("Entered the data transformation component.")
        try:
            df = pd.read_csv(self.config.data_path)
            target_column = 'price'

            num_columns,cat_columns = get_columns(df,target_column)
            
            preprocessor = self.get_preprocessor_obj(cat_columns,num_columns)

            X = df.drop([target_column],axis='columns')    #Input Features
            y = df[target_column]                          #Target Variable


            del df

            X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.8,random_state=42)

            del X,y

            X_train = preprocessor.fit_transform(X_train)
            X_test = preprocessor.transform(X_test)

            save_obj(self.config.preprocessor_obj_path,preprocessor)

            logging.info("Data transformation is completed.")
            
            return X_train,X_test,y_train,y_test
                
        except Exception as e:
            logging.error(f"Exception occurred: {type(e).__name__}, {str(e)}")
            raise CustomException(e,sys)
