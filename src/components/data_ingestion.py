import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")

class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Started")
        try:
            df = pd.read_csv("notebook/data/predictive_maintenance.csv")
            logging.info("Dataset read successfully")

            os.makedirs(os.path.dirname(self.config.raw_data_path), exist_ok = True)
            df.to_csv(self.config.raw_data_path, index = False)
            logging.info("Raw data saved to artifacts fodler")

            train_df, test_df = train_test_split(
                df,
                test_size = 0.2,
                stratify = df["Target"],
                random_state = 42
            )
            train_df.to_csv(self.config.train_data_path, index=False)
            test_df.to_csv(self.config.test_data_path, index=False)

            logging.info("Raw, Train, and Test data saved")

            return self.config.train_data_path, self.config.test_data_path

        except Exception as e:
            logging.error("Error in Data Ingestion")
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    onj = DataIngestion()
    raw_data_path = obj.initiate_data_ingestion()        

    
