from kedro.pipeline import Pipeline, node
from .nodes import _clean_score, _create_columns, _drop_col, _convert_datatypes, _split_fixtures, _save_as_csv  # Import your node functions

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=_clean_score,
            inputs="fixture_data",
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
            outputs="fixture_df_clean",
            name="convert_datatypes"
        ),
        node(
            func=_split_fixtures,
            inputs="fixture_df_clean",
            outputs=["other_fixtures", "normal_fixtures"],
            name="split_fixtures"
        ),
        node(
            func=_save_as_csv,
            inputs=["normal_fixtures", "params:fixtures_clean_filepath.normal_results"],
            outputs=None,
            name="save_normal_fixtures"
        ),
        node(
            func=_save_as_csv,
            inputs=["other_fixtures", "params:fixtures_clean_filepath.other_results"],
            outputs=None,
            name="save_other_fixtures"
        )
    ])