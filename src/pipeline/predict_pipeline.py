import os 
import sys
import pandas as pd 
import numpy as np 

from src.logger import logging 
from src.exception import CustomException
from src.utils import load_obj


class PredictPipeline:
    """
    This class is used to predict the price using a pre-trained model
    """
    def __init__(self):
        self.model_path = os.path.join('model','model.pkl')
        self.preprocessor_path = os.path.join('model','preprocessor.pkl')     

    def predict_price(self,data):
        """
        Predict the price based on input data.

        Parameters:
            data(DataFrame): The input data for prediction. 

        Returns: 
            np.array : The predicted price.
        """
        model = load_obj(self.model_path)
        preprocessor = load_obj(self.preprocessor_path)

        preprocessed_data = preprocessor.transform(data)
        score = model.predict(preprocessed_data)


        return np.around(score, decimals=2)



class CustomData:
    """
    This class is used to create a custom data object.
    """
    def __init__(self,location,total_sqft,size,area_type,balcony,bath):
        self.location = location
        self.total_sqft = total_sqft
        self.size = size
        self.area_type = area_type
        self.balcony = balcony
        self.bath = bath 

    def get_data_as_dataframe(self):
        """
        Convert the custom data object to a DataFrame.

        Returns:
            DataFrame : The DataFrame representation of the custom data object.
        """
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
            logging.error(f"An error occurred during the predicting pipeline: {e}")
            raise CustomException(e,sys)
        

