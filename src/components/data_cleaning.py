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
    """
    A data class that holds configuration information for the data cleaning process.

    Attributes:
        cleaned_data_path (str): The path where the cleaned data will be stored.
        raw_data_path (str): The path where the raw data is located.
    """
    cleaned_data_path : str = os.path.join('data','processed','clean_data.csv')
    raw_data_path : str 

class DataCleaning:
    """
    A class used to clean data.

    Attributes:
        config (DataCleaningConfig): The configuration information for the data cleaning process.
    """
    def __init__(self, config:DataCleaningConfig):
        self.config = config

    def initiate_data_cleaning(self):
        """
        The function to initiate the data cleaning process.

        Returns:
            str: The path where the cleaned data will be stored.
        """
        logging.info("Entered the data cleaning component.")
        try:
            
            df = pd.read_csv(self.config.raw_data_path)

            columns_to_keep =['location','total_sqft','size','area_type','balcony','bath', 'price']

            df = keep_required_columns(df,columns_to_keep)

            df.dropna(inplace=True)
            df.drop_duplicates(inplace=True)

            df = extract_bhk(df)

            df['total_sqft'] = df['total_sqft'].apply(conv_sqft)

            df.dropna(inplace=True)    # Drop rows where total_sqft couldn't be converted to float

            # Convert location to 'other' if it's not a common location
            df = loc_to_others(df)

            os.makedirs(os.path.dirname(self.config.cleaned_data_path),exist_ok=True)
            
            df.to_csv(self.config.cleaned_data_path,index=False)

            logging.info("Data cleaning is completed.")
            
            return self.config.cleaned_data_path
        

        except Exception as e:
            logging.error(f"Exception occurred: {type(e).__name__}, {str(e)}")
            raise CustomException(e,sys)




            
  