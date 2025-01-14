from kedro.pipeline import Pipeline, node
from .nodes import _scrape_fixture_data  # Import functions

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=_scrape_fixture_data,
            inputs="season_ids_json", # JSON file called via data catalog
            outputs="unclean_fixture_data", # DataFrame registered in data catalog
            name="scrape_fixture_data" 
        )
    ])