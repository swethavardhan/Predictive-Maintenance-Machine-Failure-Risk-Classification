import os
import sys
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object

class ThresholdModel:
    def __init__(self, model, threshold):
        self.model = model
        self.threshold = threshold

    def predict(self, X):
        proba = self.model.predict_proba(X)[:, 1]
        return (proba >= self.threshold).astype(int)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

class ModelTrainer:
    def __init__(self):
        self.model_dir = os.path.join("artifacts", "models")
        os.makedirs(self.model_dir, exist_ok=True)

    def initiate_model_training(self, train_array, test_array):
        logging.info("Model Training Started")

        try:
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            dt = DecisionTreeClassifier(
                max_depth=5,
                class_weight={0: 1, 1: 10},
                random_state=42
            )

            rf = RandomForestClassifier(
                n_estimators=200,
                class_weight={0: 1, 1: 10},
                random_state=42
            )

            ensemble = VotingClassifier(
                estimators=[('dt', dt), ('rf', rf)],
                voting='soft',
                weights=[5, 2]
            )

            ensemble.fit(X_train, y_train)
            logging.info("Ensemble model trained")

            y_proba = ensemble.predict_proba(X_test)[:, 1]
            roc_auc = roc_auc_score(y_test, y_proba)
            logging.info(f"ROC-AUC: {roc_auc}")

            thresholds = [0.5, 0.35, 0.3]

            for th in thresholds:
                y_pred = (y_proba >= th).astype(int)

                logging.info(f"\nThreshold: {th}")
                logging.info("\n" + classification_report(y_test, y_pred))
                logging.info(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

                model_wrapper = ThresholdModel(ensemble, th)

                save_object(
                    os.path.join(self.model_dir, f"ensemble_threshold_{th}.pkl"),
                    model_wrapper
                )

                logging.info(f"Model saved for threshold {th}")
            
        except Exception as e:
            logging.error("Error in Model Training")
            raise CustomException(e, sys)