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
    preprocessor_obj_path = os.path.join('model','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig

    def get_preprocessor_obj(self,cat_columns,num_columns):
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
        

    def initiate_data_transformation(self,data_path):
        logging.info("Entered the data transformation component.")
        try:
            df = pd.read_csv(data_path)
            target_column = 'price'
            num_columns,cat_columns = get_columns(df,target_column)
            print(num_columns,cat_columns)
            preprocessor = self.get_preprocessor_obj(cat_columns,num_columns)

            X = df.drop([target_column],axis='columns')
            y = df[target_column]

            del df

            X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.8,random_state=42)

            del X,y

            X_train = preprocessor.fit_transform(X_train)
            X_test = preprocessor.transform(X_test)

            save_obj(self.data_transformation_config.preprocessor_obj_path,preprocessor)

            logging.info("Data transformation is completed.")
            
            return X_train,X_test,y_train,y_test
                
        except Exception as e:
            logging.error(f"An error occurred during the data transformation process: {e}")
            raise CustomException(e,sys)
