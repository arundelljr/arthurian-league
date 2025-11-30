import pandas as pd

def merge_seasons(current_df, delta_df):

    # print(current_df.duplicated().sum())
    # current_df = current_df.drop_duplicates(subset="fixture_id", keep="last")

    current_df = pd.concat([current_df, delta_df], ignore_index=True)
    # print(current_df.duplicated().sum())

    current_df["fixture_id"] = current_df["fixture_id"].astype(str).str.strip()

    current_df = current_df.drop_duplicates(subset="fixture_id", keep="last")
    # print(delta_df.dtypes)
    # print(current_df.dtypes)
    # print(current_df.duplicated().sum())

    current_df.to_csv("data/final/all_results.csv", index=False)

    # update played and unplayed dfs
    # played games must have valid
    played_mask = current_df['home_goals'].fillna("").str.isdigit()

    played_results_df = current_df[played_mask].copy()
    unplayed_results_df = current_df[~played_mask].copy()

    played_results_df.home_goals = played_results_df.home_goals.astype(int)
    played_results_df.away_goals = played_results_df.away_goals.astype(int)

    print("updating played/unplayed results")
    played_results_df.to_csv("data/final/played_results.csv", index=False)
    unplayed_results_df.to_csv("data/final/unplayed_results.csv", index=False)
