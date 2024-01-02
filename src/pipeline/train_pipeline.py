import sys
import os
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion,DataIngestionConfig 
from src.components.data_cleaning import DataCleaning,DataCleaningConfig
from src.components.outliers import OutliersRemoval,OutliersRemovalConfig
from src.components.data_transformation import DataTransformation,DataTransformationConfig
from src.components.model_evaluation import ModelEvaluation,ModelEvaluationConfig
from src.components.model_trainer import ModelTrainer,ModelTrainerConfig

file_path : str = os.path.join('notebook','data','Bengaluru_House_Data.csv')
default_raw_data_path : str = os.path.join('data','raw','raw_data.csv')
default_cleaned_data_path : str = os.path.join('data','processed','clean_data.csv')
default_data_without_outliers_path : str = os.path.join('data','processed','data_without_outliers.csv')
preprocessor_obj_path : str = os.path.join('model','preprocessor.pkl')
default_model_obj_path : str = os.path.join('model','model.pkl')
result_path : str = os.path.join(os.getcwd(),'result.txt')


def main():
    logging.info("Entered the training pipeline.")
    try:
        #Data Ingestion
        data_ingestion_config = DataIngestionConfig(file_path,default_raw_data_path)
        data_ingestion = DataIngestion(data_ingestion_config)
        raw_data_path = data_ingestion.initiate_data_ingestion()


        #Data Cleaning
        data_cleaning_config = DataCleaningConfig(default_cleaned_data_path,raw_data_path)
        data_cleaning = DataCleaning(data_cleaning_config)
        clean_data_path = data_cleaning.initiate_data_cleaning()


        #Outliers Removal
        outlier_removal_config = OutliersRemovalConfig(default_data_without_outliers_path,clean_data_path)
        outlier_removal = OutliersRemoval(outlier_removal_config)
        data_without_outliers_path = outlier_removal.initiate_outliers_removal()


        #Data Transformation
        data_transformation_config = DataTransformationConfig(preprocessor_obj_path,data_without_outliers_path)
        data_transformation = DataTransformation(data_transformation_config)
        X_train,X_test,y_train,y_test = data_transformation.initiate_data_transformation()


        #Model Training
        model_trainer_config = ModelTrainerConfig(default_model_obj_path)
        model_trainer = ModelTrainer(model_trainer_config)
        model_obj_path,X_test,y_test = model_trainer.initiate_model_trainer(X_train,X_test,y_train,y_test)


        #Model Evaluation
        model_evaluation_config = ModelEvaluationConfig(result_path,model_obj_path)
        model_evaluation = ModelEvaluation(model_evaluation_config)
        model_evaluation.initiate_model_evaluation(X_test,y_test)

     

        logging.info("The training pipeline has been successfully completed.")

    except Exception as e:
        logging.error(f"An error occurred during the training pipeline: {e}")
        raise CustomException(e,sys)
    
if __name__ == "__main__":
    main()