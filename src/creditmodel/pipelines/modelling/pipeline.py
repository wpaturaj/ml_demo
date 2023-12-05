"""
This is a boilerplate pipeline 'modelling'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import randomized_cv_search, report_model

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=randomized_cv_search,
                inputs=["train_scd","y_train"],
                outputs="logit",
                name="model_cv_search",
            ),
            node(
                func=report_model,
                inputs=["logit","train_scd","y_train","test_scd","y_test"],
                outputs=None,
                name="report_model",
            ),
        ]
        )
