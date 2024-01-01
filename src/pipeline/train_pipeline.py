import sys
import os
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion 
from src.components.data_cleaning import DataCleaning
from src.components.outliers import OutliersRemoval
from src.components.data_transformation import DataTransformation
from src.components.model_evaluation import ModelEvaluation
from src.components.model_trainer import ModelTrainer
# create a DataIngestion object, you can specify the file path.
def main():
    logging.info("Entered the training pipeline.")
    try:
        data_ingestion = DataIngestion(os.path.join('notebook','data','Bengaluru_House_Data.csv'))
        data_cleaning = DataCleaning()
        data_transformation = DataTransformation()
        outlier_removal = OutliersRemoval()
        model_trainer = ModelTrainer()
        model_evaluation = ModelEvaluation()

        raw_data_path = data_ingestion.initiate_data_ingestion()
        clean_data_path = data_cleaning.initiate_data_cleaning(raw_data_path)
        data_path = outlier_removal.initiate_outliers_removal(clean_data_path)
        X_train,X_test,y_train,y_test = data_transformation.initiate_data_transformation(data_path)
        model_path,X_test,y_test = model_trainer.initiate_model_trainer(X_train,X_test,y_train,y_test)
        model_evaluation.initiate_model_evaluation(model_path,X_test,y_test)

        logging.info("The training pipeline has been successfully completed.")

    except Exception as e:
        logging.error(f"An error occurred during the training pipeline: {e}")
        raise CustomException(e,sys)
    
if __name__ == "__main__":
    main()