"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""
from typing import Dict, Tuple, Any

import pandas as pd
import mlflow
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


YEARS_MAPPING = {'10+ years': 10,'9 years': 9,'8 years': 8,'7 years':7,'6 years':6,
                            '5 years': 5, '4 years': 4, '3 years':3, '2 years': 2,'1 year': 1, '< 1 year':0 }

CATEGORICAL_COLUMNS = ["home_ownership", "purpose", "term"]

def process_column_names(data):
    columns = [str(i).lower().replace(" ", "_") for i in (list(data.columns))]
    data.columns = columns
    return data

def split_data(data: pd.DataFrame) -> Tuple:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters/data_science.yml.
    Returns:
        Split data.
    """
    X = data.drop(['id', 'credit_default'], axis=1)
    y = data['credit_default']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1
    )
    return X_train, X_test, y_train, y_test


def fit_feature_processing(data: pd.DataFrame) -> Tuple[Any, Any, Any, pd.DataFrame]:
    """
    Fit and transform the input data using a series of preprocessing steps:
    1. Map 'years_in_current_job' column using YEARS_MAPPING.
    2. Impute missing values using the most frequent strategy.
    3. Perform one-hot encoding on categorical columns.
    4. Concatenate one-hot encoded features with other columns.
    5. Scale the data using StandardScaler.

    Args:
        data (pd.DataFrame): Input DataFrame containing the features.

    Returns:
        Tuple[Any, Any, Any, pd.DataFrame]: Tuple containing the fitted imputer, encoder, scaler,
        and the transformed and scaled DataFrame.
    
    """
    data['years_in_current_job']=data['years_in_current_job'].map(YEARS_MAPPING)
    #Imputing missing values
    imputer = SimpleImputer(strategy="most_frequent").set_output(transform="pandas").fit(data)
    imputed_data = imputer.transform(data)
    #One Hot Encoding
    encoder = OneHotEncoder(sparse_output=False).set_output(transform="pandas").fit(imputed_data[CATEGORICAL_COLUMNS])
    data_hot_encoded = encoder.transform(imputed_data[CATEGORICAL_COLUMNS])
    data_other_cols = imputed_data.drop(columns=CATEGORICAL_COLUMNS)
    encoded_data = pd.concat([data_hot_encoded, data_other_cols], axis=1)
    # Scaling
    scaler = StandardScaler().set_output(transform="pandas").fit(encoded_data)
    scaled_data = scaler.transform(encoded_data)
    return imputer, encoder, scaler, scaled_data


def transform_feature_processing(data: pd.DataFrame, imputer: Any, encoder: Any, scaler: Any) -> pd.DataFrame:
    """
    Transform the input data using pre-fitted imputer, encoder, and scaler.

    Args:
        data (pd.DataFrame): Input DataFrame containing the features.
        imputer (Any): Fitted imputer object.
        encoder (Any): Fitted encoder object.
        scaler (Any): Fitted scaler object.

    Returns:
        pd.DataFrame: Transformed and scaled DataFrame.
    """
    data['years_in_current_job']=data['years_in_current_job'].map(YEARS_MAPPING)
    imputed_data = imputer.transform(data)
    data_hot_encoded = encoder.transform(imputed_data[CATEGORICAL_COLUMNS])
    data_other_cols = imputed_data.drop(columns=CATEGORICAL_COLUMNS)
    encoded_data = pd.concat([data_hot_encoded, data_other_cols], axis=1)
    scaled_data = scaler.transform(encoded_data)
    return scaled_data


def visualize_data(X) -> None:
    """
    Visualize the correlation matrix of the input DataFrame and log the figure using MLflow.

    Args:
        X (pd.DataFrame): Input DataFrame.

    Returns:
        None
    """
    fig = plt.figure(figsize = (25,25))
    sns.heatmap(X.corr(numeric_only=True), annot = True, vmax = 1, vmin = -1, square = True, fmt='.1f')
    mlflow.log_figure(fig, 'correlation_matrix.png')
