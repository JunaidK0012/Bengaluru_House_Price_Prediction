"""
This module contains classes and functions for data ingestion.
"""

import pandas as pd 
import os 
import sys 

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

@dataclass 
class DataIngestionConfig:
    raw_data_path : str = os.path.join('data','raw','raw_data.csv')

class DataIngestion:
    def __init__(self,file_path : str):
        self.DataIngestionConfig = DataIngestionConfig()
        self.file_path = file_path

    def initiate_data_ingestion(self):
        """
        The function to initiate the data ingestion process.
        
        Returns:
            str: The path where the raw data is stored.
        """

        logging.info("Entered the data ingestion component.")
        try:
            # Check if the file exists
            if not os.path.isfile(self.file_path):
                raise FileNotFoundError("The file does not exist.")
            
            df = pd.read_csv(self.file_path)

            # Check if the file is not empty
            if df.empty:
                raise ValueError("The file is empty.")
            
            # Check if the file has the expected columns
            expected_columns = ['location','total_sqft','size','area_type','balcony','bath', 'price']
            if not set(expected_columns).issubset(df.columns):
                raise ValueError("The file does not have the expected columns.")

            os.makedirs(os.path.dirname(self.DataIngestionConfig.raw_data_path),exist_ok=True)
            df.to_csv(self.DataIngestionConfig.raw_data_path,index=False)

            logging.info("Data Ingestion is completed.")

            return self.DataIngestionConfig.raw_data_path
            
        except Exception as e:
            logging.error(f"Exception occurred: {type(e).__name__}, {str(e)}")
            raise CustomException(e,sys)
        



