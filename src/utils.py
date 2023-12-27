import os 
import sys 
import pandas as pd 
import numpy as np 
from src.logger import logging
import joblib

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
    
def remove_outliers(data):
    try:
        df = pd.DataFrame()
        for key,subdf in data.groupby('location'):
            m = subdf['price_per_sqft'].mean()
            std = subdf['price_per_sqft'].std()
            reduced_df = subdf[(subdf['price_per_sqft']>=(m-std)) & (subdf['price_per_sqft']<=(m+std))]
            df = pd.concat([df,reduced_df],ignore_index=True)
        return df
    except Exception as e:
        logging.error(f"Exception occured : {e}")
        raise CustomException(e,sys)
    
def remove_bhk_outliers(data):
    try:
        exclude_indices = np.array([])
        for loc,loc_df in data.groupby('location'):
            bhk_stats = loc_df.groupby('size').apply(cal_stats).to_dict()
            for bhk,bhk_df in loc_df.groupby('size'):
                stats = bhk_stats.get(bhk-1)
                if stats and stats['count']>5:
                    exclude_indices = np.append(exclude_indices, bhk_df[bhk_df['price_per_sqft'] < stats['mean']].index.values)
        return data.drop(exclude_indices, axis='index')

    except Exception as e:
        logging.error(f'Exception occured : {e}')
        raise CustomException(e,sys)
    
def cal_stats(data):
        return {
        'mean': np.mean(data['price_per_sqft']),
        'std': np.std(data['price_per_sqft']),
        'count': data.shape[0]
    }

def get_columns(data,target_column):
    try:
        num_columns = []
        cat_columns = []
        for x in data.columns:
            if x == target_column:
                pass
            else:
                if data[x].dtype == "O":
                    cat_columns.append(x)
                else:
                    num_columns.append(x)

        return num_columns,cat_columns
    
    except Exception as e:
        raise CustomException(e,sys)
    
def save_obj(file_path,obj):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)

        joblib.dump(obj,file_path)
        
    except Exception as e:
        raise CustomException(e,sys)

        
    
