from kedro.pipeline import Pipeline, node
from .nodes import _ALFIE_rating # Import functions

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=_ALFIE_rating,
            inputs=["normal_fixture_data", "params:ALFIE_rating.new_col", "params:ALFIE_rating.homescore", "params:ALFIE_rating.awayscore"], # DataFrame called via data catalog, column names called from parameters
            outputs="ALFIE_fixture_data", # DataFrame registered in data catalog
            name="add_ALFIE_rating"
        )
    ])