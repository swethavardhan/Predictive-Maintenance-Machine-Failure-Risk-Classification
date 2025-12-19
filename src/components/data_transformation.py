import os
import sys 
import numpy as np 
import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import ADASYN

from src.logger import logging
from src.exception import CustomException

class DataTransformation:
    def initiate_data_transformation(self, train_path, test_path):
        logging.info("Data Transformation Started")

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            drop_cols = ['UDI', 'Product ID', 'Failure Type']
            train_df.drop(columns=drop_cols, inplace=True)
            test_df.drop(columns=drop_cols, inplace=True)

            le = LabelEncoder()
            train_df['Type_encoded'] = le.fit_transform(train_df['Type'])
            test_df['Type_encoded'] = le.transform(test_df['Type'])

            train_df.drop(columns=['Type'], inplace=True)
            test_df.drop(columns=['Type'], inplace=True)

            X_train = train_df.drop('Target', axis=1)
            y_train = train_df['Target']
            X_test = test_df.drop('Target', axis=1)
            y_test = test_df['Target']

            X_train.columns = X_train.columns.astype(str).str.replace('[\\[\\]<]', '', regex=True)
            X_test.columns = X_test.columns.astype(str).str.replace('[\\[\\]<]', '', regex=True)

            adasyn = ADASYN(random_state=42)
            X_train_res, y_train_res = adasyn.fit_resample(X_train, y_train)

            logging.info(f"After ADASYN class counts: {np.bincount(y_train_res)}")

            train_array = np.c_[X_train_res.to_numpy(), y_train_res.to_numpy()]
            test_array = np.c_[X_test.to_numpy(), y_test.to_numpy()]

            return train_array, test_array
        
        except Exception as e:
            logging.error("Error in Data Transformation")
            raise CustomException(e, sys)