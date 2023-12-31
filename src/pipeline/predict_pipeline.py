import os 
import sys
import pandas as pd 
import numpy as np 

from src.logger import logging 
from src.exception import CustomException
from src.utils import load_obj


class PredictPipeline:
    def predict_price(self,data):
        model_path = os.path.join('model','model.pkl')
        preprocessor_path = os.path.join('model','preprocessor.pkl')

        model = load_obj(model_path)
        preprocessor = load_obj(preprocessor_path)

        preprocessed_data = preprocessor.transform(data)
        score = model.predict(preprocessed_data)


        return np.around(score, decimals=2)



class CustomData:
    def __init__(self,location,total_sqft,size,area_type,balcony,bath):
        self.location = location
        self.total_sqft = total_sqft
        self.size = size
        self.area_type = area_type
        self.balcony = balcony
        self.bath = bath 

    def get_data_as_dataframe(self):
        try:
            data_to_dict = {
                'location' : [self.location],
                'total_sqft' : [self.total_sqft],
                'size' : [self.size],
                'area_type' : [self.area_type],
                'balcony' : [self.balcony],
                'bath' : [self.bath]
            }

            return pd.DataFrame(data_to_dict)

         

        except Exception as e:
            raise CustomException(e,sys)