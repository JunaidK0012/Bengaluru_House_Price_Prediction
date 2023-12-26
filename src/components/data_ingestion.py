import pandas as pd 
import os 
import sys 

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

from src.components.data_cleaning import DataCleaningConfig
from src.components.data_cleaning import DataCleaning

@dataclass 
class DataIngestionConfig:
    raw_data_path = os.path.join('data','raw','raw_data.csv')

class DataIngestion:
    def __init__(self):
        self.DataIngestionConfig = DataIngestionConfig()

    def initiate_model_trainer(self):
        logging.info("Entered the data ingestion component.")
        try:
            df = pd.read_csv(os.path.join('notebook', 'data', 'Bengaluru_House_Data.csv'))
            logging.info("Read the dataset as dataframe.")

            os.makedirs(os.path.dirname(self.DataIngestionConfig.raw_data_path),exist_ok=True)
            df.to_csv(self.DataIngestionConfig.raw_data_path,index=False)

            logging.info("Data Ingestion is completed.")

            return self.DataIngestionConfig.raw_data_path
            
        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    obj = DataIngestion()
    raw_data_path = obj.initiate_model_trainer()

    data_cleaner = DataCleaning()
    data_cleaner.initiate_data_cleaning(raw_data_path)