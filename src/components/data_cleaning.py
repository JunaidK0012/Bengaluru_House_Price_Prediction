import pandas as pd
import numpy as np
import os 
import sys 

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import keep_required_columns,extract_bhk,conv_sqft,loc_to_others

@dataclass
class DataCleaningConfig:
    processed_data_path = os.path.join('data','processed','clean_data.csv')

class DataCleaning:
    def __init__(self):
        self.data_cleaning_config = DataCleaningConfig()

    def initiate_data_cleaning(self,raw_data_path):
        logging.info("Entered the data cleaning component.")
        try:
            
            df = pd.read_csv(raw_data_path)

            columns_to_keep =['area_type','balcony','location', 'size','total_sqft', 'bath', 'price']

            df = keep_required_columns(df,columns_to_keep)

            df.dropna(inplace=True)
            df.drop_duplicates(inplace=True)

            df = extract_bhk(df)

            df['total_sqft'] = df['total_sqft'].apply(conv_sqft)

            df.dropna(inplace=True)    #the 'total_sqft' values which didn't got converted to float returned None

            df = loc_to_others(df)

            os.makedirs(os.path.dirname(self.data_cleaning_config.processed_data_path),exist_ok=True)
            
            df.to_csv(self.data_cleaning_config.processed_data_path,index=False)

            logging.info("Data cleaning is completed.")
            
            return self.data_cleaning_config.processed_data_path
        

        except Exception as e:
            logging.error(f"An error occurred during the data cleaning process: {e}")
            raise CustomException(e,sys)




            
  