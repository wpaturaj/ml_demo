"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import process_column_names, split_data, fit_feature_processing, transform_feature_processing,visualize_data

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=process_column_names,
                inputs=["train"],
                outputs="train_col_clean",
                name="clean_train_columns",
                ),
            node(
                func=split_data,
                inputs="train_col_clean",
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=fit_feature_processing,
                inputs=["X_train"],
                outputs=["imputer", "encoder", "scaler", "train_scd"],
                name="fit_feature_enginerring",
            ),
            node(
                func=transform_feature_processing,
                inputs=["X_test", "imputer", "encoder", "scaler"],
                outputs="test_scd",
                name="transform_feature_processing",
            ),
            node(
                func=visualize_data,
                inputs="train_scd",
                outputs=None,
                name="visualize_data"
            )
        ])
