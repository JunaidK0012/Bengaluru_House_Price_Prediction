import os 
import sys 
import pandas as pd 
import numpy as np 
from src.logger import logging

from src.exception import CustomException

def keep_required_columns(data,columns_to_keep):
    try:
        data = data[columns_to_keep]
        return data

    except Exception as e:
        missing_columns = list(set(columns_to_keep) - set(data.columns))
        logging.error(f"Exception occurred :The following required columns are missing from the data: {missing_columns}")
        raise CustomException(e,sys,missing_columns)
    
def extract_bhk(data):
    try:
        data['size'] = data['size'].apply(lambda x: int(x.split(' ')[0]))
        return data
    
    except Exception as e:
        logging.error(f"Exception occured : {e}")
        raise CustomException(e,sys)
    
def conv_sqft(x):
    try:
        tokens = x.split('-')
        if len(tokens)==2:
            return (float(tokens[0]) + float(tokens[1]) /2 )
        try:
            return float(x)
        except:
            return None
        
    except Exception as e:
        logging.error(f"Exception occured : {e}")
        raise CustomException(e,sys)
    
def loc_to_others(data):
    try:
        data['location'] = data['location'].apply(lambda x : x.strip())
        location_stats = data['location'].value_counts(ascending=False)
        location_stats_less_than_10 = location_stats[location_stats<=10]

        data['location'] = data['location'].apply(lambda x : 'others' if x in location_stats_less_than_10 else x)

        return data
    
    except Exception as e:
        logging.error(f"Exception occured : {e}")
        raise CustomException(e,sys)
        

        
    
