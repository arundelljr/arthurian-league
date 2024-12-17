from kedro.pipeline import Pipeline, node
from .nodes import _scrape_fixture_data, _save_as_csv  # Import your node functions

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=_scrape_fixture_data,
            inputs="season_ids_data",
            outputs="fixture_df",
            name="scrape_fixture_data"
        ),
        node(
            func=_save_as_csv,
            inputs=["fixture_df", "params:fixture_data_filepath"],
            outputs=None,
            name="save_fixture_df"
        )
    ])