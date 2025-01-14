from kedro.pipeline import Pipeline, node
from .nodes import _get_url_soup, _extract_season_ids  # Import functions

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=_get_url_soup,
            inputs="params:fa_urls.seasons_url", # URL called from parameters YAML
            outputs="soup",
            name="get_fa_url_soup"
        ),
        node(
            func=_extract_season_ids,
            inputs="soup",
            outputs="season_ids_json", # Dictionary is saved as JSON file registered in data catalog  
            name="extract_al_season_ids"
        )
    ])