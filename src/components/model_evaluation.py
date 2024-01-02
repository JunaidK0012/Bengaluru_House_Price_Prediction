import os 
import sys 

from src.exception import CustomException
from src.logger import logging 
from dataclasses import dataclass
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from src.utils import load_obj

@dataclass
class ModelEvaluationConfig:
    """
    A data class that holds configuration information for the model evaluation process. 

    Attributes:
        result_path : The path where the result.txt will be stored.
        model_obj_path : The path where the trained model is stored.
    """
    result_path : str 
    model_obj_path : str

class ModelEvaluation:
    """
    A class for model evaluation.

    Attributes:
        config(ModelEvaluationConfig) : The configuration information for the model evaluation process
    """
    def __init__(self,config:ModelEvaluationConfig):
        self.config = config
    
    def initiate_model_evaluation(self,X_test,y_test):
        """
        The function to initiate the model evaluation process.

        Parameters:
            X_test (ndarray) : Test features
            Y_test (ndarray) : Test labels
        """
        logging.info("Starting the model evaluation.")
        try:
            model = load_obj(self.config.model_obj_path)
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test,y_pred)
            mse = mean_squared_error(y_test,y_pred)
            r2 = r2_score(y_test,y_pred)

            logging.info("Saving all the metrics results in a results.txt file.")
            with open(self.config.result_path, "w") as f:
                f.write(f'Evaluation metrics results: \n')
                f.write(f"Mean Squared Error: {mse:.2f}\n")
                f.write(f"R-squared Score: {r2:.2f}\n")
                f.write(f"Mean Absolute Error: {mae:.2f}\n")

            logging.info("Model Evaluation has been completed.")
                

        except Exception as e:
            logging.error(f"Exception occurred: {type(e).__name__}, {str(e)}")
            raise CustomException(e,sys)
        