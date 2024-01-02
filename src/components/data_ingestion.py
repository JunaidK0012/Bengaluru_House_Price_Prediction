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
    """
    A data class that holds configuration information for the data ingestion process.

    Attributes:
        file_path (str): The path from where the raw data will be taken.
        raw_data_path (str): The path where the raw data will stored.
    """
    file_path : str
    raw_data_path : str 

class DataIngestion:
    """
    A class used to ingest data.

    Attributes:
        config (DataIngestionCOnfig): The configuration information for the data ingestion process.
    """
    def __init__(self,config : DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self):
        """
        The function to initiate the data ingestion process.
        
        Returns:
            str: The path where the raw data is stored.
        """

        logging.info("Entered the data ingestion component.")
        try:
            # Check if the file exists
            if not os.path.isfile(self.config.file_path):
                raise FileNotFoundError("The file does not exist.")
            
            df = pd.read_csv(self.config.file_path)

            # Check if the file is not empty
            if df.empty:
                raise ValueError("The file is empty.")
            
            # Check if the file has the expected columns
            expected_columns = ['location','total_sqft','size','area_type','balcony','bath', 'price']
            if not set(expected_columns).issubset(df.columns):
                raise ValueError("The file does not have the expected columns.")

            os.makedirs(os.path.dirname(self.config.raw_data_path),exist_ok=True)
            df.to_csv(self.config.raw_data_path,index=False)

            logging.info("Data Ingestion is completed.")

            return self.config.raw_data_path
            
        except Exception as e:
            logging.error(f"Exception occurred: {type(e).__name__}, {str(e)}")
            raise CustomException(e,sys)
        



