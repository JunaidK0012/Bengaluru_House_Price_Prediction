import pandas as pd 
import os 
import sys 

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

@dataclass 
class DataIngestionConfig:
    raw_data_path = os.path.join('data','raw','raw_data.csv')

class DataIngestion:
    def __init__(self):
        self.DataIngestionConfig = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion component.")
        try:
            df = pd.read_csv(os.path.join('notebook', 'data', 'Bengaluru_House_Data.csv'))

            os.makedirs(os.path.dirname(self.DataIngestionConfig.raw_data_path),exist_ok=True)
            df.to_csv(self.DataIngestionConfig.raw_data_path,index=False)

            logging.info("Data Ingestion is completed.")

            return self.DataIngestionConfig.raw_data_path
            
        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            raise CustomException(e,sys)
        



