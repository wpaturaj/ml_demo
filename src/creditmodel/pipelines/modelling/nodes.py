"""
This is a boilerplate pipeline 'modelling'
generated using Kedro 0.18.14
"""
import pandas as pd
import numpy as np
import mlflow

from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

def randomized_cv_search(
    train_x: pd.DataFrame,
    train_y: pd.Series
) -> LogisticRegression:
    """
    Perform randomized cross-validated hyperparameter search for a Logistic Regression model.

    Args:
        train_x (pd.DataFrame): Training feature set.
        train_y (pd.Series): Training target labels.

    Returns:
        LogisticRegression: The best-fit Logistic Regression model.
    """
    # Create a base classifier to search over
    clf_logit = LogisticRegression(random_state=42)

    # Define parameter distribution
    logit_param_grid = {
        'C': [0.1, 1, 5, 10],
        'l1_ratio' : np.arange(0, 1, 0.2),
        'solver': ['newton-cg', 'liblinear', 'sag', 'saga'],
        'max_iter': [2000],
        'class_weight': [None, 'balanced'],
        'penalty': ['l1', 'l2', 'elasticnet'],
    }

    # Create randomized search instance
    rclf = RandomizedSearchCV(
        clf_logit,
        param_distributions=logit_param_grid,
        random_state=42,
        n_iter=5,
        refit=True,
        verbose=0,
        n_jobs=2,
        scoring='f1',
    )
    # Fit cv x n_iter number of models
    rclf.fit(train_x, train_y)
    results = pd.DataFrame(rclf.cv_results_)
    results = results[['params', 'mean_test_score', 'std_test_score']]
    results = results.values
    for run in results:
        with mlflow.start_run(nested=True):
            mlflow.log_params(run[0])
            mlflow.log_metric("f1", run[1])

    return rclf.best_estimator_


def report_model(model: LogisticRegression, train_x: pd.DataFrame, train_y: pd.Series, test_x: pd.DataFrame, test_y: pd.Series) -> None:
    """
    Log metrics and parameters for a given model on training and test sets.

    Args:
        model (LogisticRegression): The trained Logistic Regression model.
        train_x (pd.DataFrame): Training feature set.
        train_y (pd.Series): Training target labels.
        test_x (pd.DataFrame): Test feature set.
        test_y (pd.Series): Test target labels.

    Returns:
        None
    """
    mlflow.log_metric("f1_test", f1_score(test_y, model.predict(test_x)))
    mlflow.log_metric("f1_train", f1_score(train_y, model.predict(train_x)))
    mlflow.log_params(model.get_params())
    return None
