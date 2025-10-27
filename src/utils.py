import os
import sys
import dill
import time
from sklearn.metrics import r2_score
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import GridSearchCV

def save_object(file_path: str, obj: object) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        logging.info('Error in saving object')
        raise CustomException(e, sys)

def load_object(file_path: str) -> object:
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        logging.info('Error in loading object')
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
# def evaluate_models(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        total_start_time = time.time()
        
        for i in range(len(list(models))):
            iteration_start_time = time.time()
            model_name = list(models.keys())[i]
            print(f'Evaluating MODEL NAME: {model_name}')
            logging.info(f'Starting evaluation for model: {model_name}')
            
            model = list(models.values())[i]
            param_settings = params[list(models.keys())[i]]
            
            # Time GridSearchCV
            gs_start_time = time.time()
            gs = GridSearchCV(model, param_settings, cv=3)
            gs.fit(X_train, y_train)
            gs_time = time.time() - gs_start_time
            
            print(f'Best Params for {model_name}: {gs.best_params_}')
            print(f'GridSearchCV completed in {gs_time:.2f} seconds')
            logging.info(f'GridSearchCV for {model_name} completed in {gs_time:.2f} seconds')
            
            # Time final model training
            training_start_time = time.time()
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            training_time = time.time() - training_start_time
            
            print(f'Model {model_name} trained in {training_time:.2f} seconds')
            logging.info(f'Final training for {model_name} completed in {training_time:.2f} seconds')
            
            # Time prediction
            prediction_start_time = time.time()
            y_test_pred = model.predict(X_test)
            prediction_time = time.time() - prediction_start_time
            
            test_model_score = r2_score(y_test, y_test_pred)
            iteration_time = time.time() - iteration_start_time
            
            print(f'Prediction completed in {prediction_time:.2f} seconds')
            print(f'Total time for {model_name}: {iteration_time:.2f} seconds')
            logging.info(f'Prediction for {model_name} completed in {prediction_time:.2f} seconds')
            logging.info(f'Total iteration time for {model_name}: {iteration_time:.2f} seconds')
            
            report[model_name] = test_model_score
        
        total_time = time.time() - total_start_time
        print(f'Total evaluation time: {total_time:.2f} seconds')
        logging.info(f'Total model evaluation time: {total_time:.2f} seconds')
        
        return report
    except Exception as e:
        logging.info('Error in evaluating models')
        raise CustomException(e, sys)

