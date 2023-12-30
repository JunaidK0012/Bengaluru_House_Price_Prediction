import os 
import sys 

from src.exception import CustomException
from src.logger import logging 
from dataclasses import dataclass
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from src.utils import load_obj

@dataclass
class ModelEvaluationConfig:
    result_path = os.path.join(os.getcwd(),'result.txt')

class ModelEvaluation:
    def __init__(self):
        self.model_evaluation_config = ModelEvaluationConfig()
    
    def initiate_model_evaluation(self,model_obj_path,X_test,y_test):
        logging.info("Starting the model evaluation.")
        try:
            model = load_obj(model_obj_path)
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test,y_pred)
            mse = mean_squared_error(y_test,y_pred)
            r2 = r2_score(y_test,y_pred)

            logging.info("Saving all the metrics results in a results.txt file.")
            with open(self.model_evaluation_config.result_path, "w") as f:
                f.write(f'Evaluation metrics results: \n')
                f.write(f"Mean Squared Error: {mse:.2f}\n")
                f.write(f"R-squared Score: {r2:.2f}\n")
                f.write(f"Mean Absolute Error: {mae:.2f}\n")

            logging.info("Model Evaluation has been completed.")
                

        except Exception as e:
            logging.error(f"Error occured: {e}")
            raise CustomException(e,sys)
        