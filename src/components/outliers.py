import os 
import sys 
import pandas as pd 
import numpy as np 

from src.logger import logging 
from src.exception import CustomException
from dataclasses import dataclass
from src.utils import remove_outliers,remove_bhk_outliers

@dataclass
class OutliersRemovalConfig:
    data_without_outliers = os.path.join('data','processed','data_without_outliers.csv')

class OutliersRemoval:
    def __init__(self):
        self.outliers_removal_config = OutliersRemovalConfig

    def initiate_outliers_removal(self,clean_data_path):
        logging.info("Entered the outlier removal component.")
        try:
            df = pd.read_csv(clean_data_path)
            df['price_per_sqft'] = df['price']*100000/df['total_sqft']

            df = df[df['total_sqft']/df['size']>300]          #a single bedroom should have a minimum of 300 sqft.
            df = remove_outliers(df)
            df = df[df['bath']<=df['size']+1]
            df = remove_bhk_outliers(df)

            df.drop(['price_per_sqft'],axis='columns',inplace=True)

            df.to_csv(self.outliers_removal_config.data_without_outliers,index=False)

            logging.info("The outlier removal process has been completed.")

            return self.outliers_removal_config.data_without_outliers
        
        except Exception as e:
            logging.error(f"An error occurred during the outlier removing process: {e}")
            raise CustomException(e,sys)
        