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
    """
    A data class that holds configuration information for the outlier removal process.

    Attributes:
        data_without_outliers_path (str): The path where the cleaned data without outliers will be stored.
        clean_data_path (str): The path where the cleaned data is located.
    """
    data_without_outliers_path : str = os.path.join('data','processed','data_without_outliers.csv')
    clean_data_path : str

class OutliersRemoval:
    """
    A class used to remove outliers from data.

    Attributes:
        config (OutliersRemovalConfig): The configuration information for the data cleaning process.
    """
    def __init__(self,config:OutliersRemovalConfig):
        self.config = config

    def initiate_outliers_removal(self) -> str:
        """
        The function to initiate the outlier removal process

        Returns:
            str: the path where the cleaned data without outliers will be stored.
        """
        logging.info("Entered the outlier removal component.")
        try:
            df = pd.read_csv(self.config.clean_data_path)
            df['price_per_sqft'] = df['price']*100000/df['total_sqft']

            df = df[df['total_sqft']/df['size']>300]       #a single bedroom should have a minimum of 300 sqft.
            df = remove_outliers(df)                       # removing outliers using mean and standard deviation.
            df = df[df['bath']<=df['size']+1]
            
            df = remove_bhk_outliers(df)   #removing the data for same location,where the price of (for example) 3bhk  is less than 2bhk(with same square ft area).

            df.drop(['price_per_sqft'],axis='columns',inplace=True)

            df.to_csv(self.config.data_without_outliers_path,index=False)

            logging.info("The outlier removal process has been completed.")

            return self.config.data_without_outliers_path
        
        except Exception as e:
            logging.error(f"Exception occurred: {type(e).__name__}, {str(e)}")
            raise CustomException(e,sys)
        