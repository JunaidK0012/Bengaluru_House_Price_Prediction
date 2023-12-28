import os 
import sys
import pandas as pd 
import numpy as np 

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_obj
 
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV,ShuffleSplit,cross_val_score



@dataclass
class ModelTrainerConfig:
    model_obj_path = os.path.join('model','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,X_train,X_test,y_train,y_test):
        logging.info("Entered the model training component.")
        try:
            models = self.get_models()
            parameters = self.get_parameters()

            cv = ShuffleSplit(n_splits=5, test_size=0.2)
            result = {}
            for model_name,model in models.items():
                grid_search = GridSearchCV(estimator=model,param_grid=parameters[model_name],cv=cv,n_jobs=-1, verbose=1)
                grid_search.fit(X_train,y_train)

                best_params = grid_search.best_params_

                best_model = model.set_params(**best_params)

                best_model.fit(X_train,y_train)

                score = best_model.score(X_test,y_test)

                result[model_name]=score
          

                print(f'The best hyperparameters for {model_name} are: {best_params}')
                print(f'The accuracy of the {model_name} model is: {score}')

                del best_model

            print(result)

            final_model = LinearRegression()
            final_model.fit(X_train,y_train)

            save_obj(self.model_trainer_config.model_obj_path,final_model)

            logging.info("Model Training is completed.")

            return self.model_trainer_config.model_obj_path,X_test,y_test
             
                
        except Exception as e:
            logging.error(f"An error occurred during the model training process: {e}")
            raise CustomException(e,sys)
        

    def get_models(self):
        """Returns the models to be trained."""
        return {
            'Linear Regression' : LinearRegression(),
            'Lasso' : Lasso(),
            'Ridge' : Ridge(),
            'Random Forest Regressor' : RandomForestRegressor()
        }
    
    def get_parameters(self):
        """Returns the hyperparameters for each model."""
        return {
            'Linear Regression': {
                'fit_intercept': [True, False]
                },
            'Lasso': {
                'alpha': [0.1,0.5],
                'fit_intercept': [True, False],
                'selection': ['cyclic', 'random']  
                },
            'Ridge': {
                'alpha': [0.6,0.4, 0.5],
                'fit_intercept': [True, False]
                },
            'Random Forest Regressor': {
                'n_estimators': [15,18,20],
                'min_samples_split': [18,20]   
                }
        }
