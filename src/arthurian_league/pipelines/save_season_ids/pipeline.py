from kedro.pipeline import Pipeline, node
from .nodes import _get_url_soup, _extract_season_ids, _save_to_json  # Import your node functions

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=_get_url_soup,
            inputs="params:fa_urls.seasons_url",
            outputs="soup",
            name="get_fa_url_soup"
        ),
        node(
            func=_extract_season_ids,
            inputs="soup",
            outputs="season_ids",
            name="extract_al_season_ids"
        ),
        node(
            func=_save_to_json,
            inputs=["season_ids", "params:season_ids_filepath"],
            outputs=None,
            name="save_season_ids"
        )
    ])