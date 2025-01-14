from kedro.pipeline import Pipeline, node
from .nodes import _clean_score, _create_columns, _drop_col, _convert_datatypes, _split_fixtures  # Import functions

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=_clean_score,
            inputs="unclean_fixture_data", # DataFrame called via data catalog
            outputs="fixture_df_1",
            name="clean_score"
        ),
        node(
            func=_create_columns,
            inputs="fixture_df_1",
            outputs="fixture_df_2",
            name="create_columns"
        ),
        node(
            func=_drop_col,
            inputs="fixture_df_2",
            outputs="fixture_df_3",
            name="drop_columns"
        ),
        node(
            func=_convert_datatypes,
            inputs="fixture_df_3",
            outputs="clean_fixture_data", # DataFrame registered in data catalog
            name="convert_datatypes"
        ),
        node(
            func=_split_fixtures,
            inputs="clean_fixture_data", # DataFrame called via data catalog
            outputs=["other_fixture_data", "normal_fixture_data"], # DataFrames registered in data catalog
            name="split_fixtures"
        )
    ])