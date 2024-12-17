from kedro.pipeline import Pipeline, node
from .nodes import _choose_columns, _reverse_fixtures, _stack_fixtures, _group_fixtures

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=_choose_columns,
            inputs="ALFIE_fixtures",
            outputs="main_df",
            name="trim_columns"
        ),
        node(
            func=_reverse_fixtures,
            inputs="main_df",
            outputs="reversed_df",
            name="reverse_fixtures"
        ),
        node(
            func=_stack_fixtures,
            inputs=["main_df", "reversed_df"],
            outputs="stacked_ALFIE_fixtures",
            name="stack_fixtures"
        ),
        node(
            func=_group_fixtures,
            inputs="stacked_ALFIE_fixtures",
            outputs="grouped_ALFIE_fixtures",
            name="group_fixtures"
        )
    ])
