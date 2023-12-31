import os 
import sys
import matplotlib.pyplot as plt
import numpy as np

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_obj

from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV,ShuffleSplit


@dataclass
class ModelTrainerConfig:
    """
    A data class that holds configuration information for the model training process.

    Attributes:
        model_obj_path : The path where the trained model will be stored.
    """
    model_obj_path : str 

class ModelTrainer:
    """
    A class used for model training.

    Attributes:
        config (ModelTrainerConfig) : The configuration information for the model training process.
    """
    def __init__(self, config:ModelTrainerConfig):
        self.config = config

    def initiate_model_trainer(self,X_train,X_test,y_train,y_test):
        """
        The function to initiate the model training process.

        Parameters:
            X_train (ndarray) : Training features
            X_test (ndarray) : Test features
            Y_train (ndarray) : Training labels
            Y_test (ndarray) : Test labels

        Returns:
            str : path to the trained model
            ndarray : Test features
            ndarray : Test labels
        """
        logging.info("Entered the model training component.")
        try:
            models = self.get_models()
            parameters = self.get_parameters()

            cv = ShuffleSplit(n_splits=5, test_size=0.2)
            result = {}
            best_model = None
            best_score = 0
            for model_name,model in models.items():
                grid_search = GridSearchCV(estimator=model,param_grid=parameters[model_name],cv=cv,n_jobs=-1, verbose=2)
                grid_search.fit(X_train,y_train)

                best_params = grid_search.best_params_

                current_model = model.set_params(**best_params)

                current_model.fit(X_train,y_train)

                score = current_model.score(X_test,y_test)

                result[model_name]=score
          

                print(f'The best hyperparameters for {model_name} are: {best_params}')
                print(f'The accuracy of the {model_name} model is: {score}')

                if score > best_score:
                    best_score = score
                    best_model = current_model

            print(result)

            logging.info(f'The model with the highest score is = {best_model} : {best_score}')
            final_model = best_model.fit(X_train,y_train)
            


            save_obj(self.config.model_obj_path,final_model)

            logging.info("Model Training is completed.")

            return self.config.model_obj_path,X_test,y_test
             
                
        except Exception as e:
            logging.error(f"Exception occurred: {type(e).__name__}, {str(e)}")
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
                'fit_intercept': [True, False]
                },
            'Ridge': {
                'alpha': [0.6],
                'fit_intercept': [True, False]
                },
            'Random Forest Regressor': {
                'n_estimators': [20,25,30],  # Number of trees in the forest
                'max_depth': [None, 10, 20, 30, 40, 50],  # Maximum depth of the tree
                'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
                'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required to be at a leaf node
                'max_features': ['sqrt'],  # Number of features to consider when looking for the best split
                'bootstrap': [True, False]  
                }
        }
