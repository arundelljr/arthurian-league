from kedro.pipeline import Pipeline, node
from .nodes import _ALFIE_rating, _save_as_csv

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=_ALFIE_rating,
            inputs=["normal_fixtures", "params:ALFIE_rating.new_col", "params:ALFIE_rating.homescore", "params:ALFIE_rating.awayscore"],
            outputs="ALFIE_fixtures",
            name="add_ALFIE_rating"
        ),
        node(
            func=_save_as_csv,
            inputs=["ALFIE_fixtures", "params:ALFIE_rating.filepath"],
            outputs=None,
            name="save_ALFIE_fixtures"
        )
    ])