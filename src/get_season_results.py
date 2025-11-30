import json
import pandas as pd
import os
from selenium import webdriver
from helper_functions.transformation import transform_season
from helper_functions.season_parsing import scrape_season
from helper_functions.merge_seasons import merge_seasons

"""
Checks which seasons have been scraped already,
scrapes unscraped seasons and
rescrapes all of current season in case of updates.
"""
# load season ids, info and current results table
with open("data/raw/season_ids.json", "r") as f:
    season_ids = json.load(f)

with open("data/raw/seasons_info.json", "r") as f:
    seasons_info = json.load(f)

if os.path.exists("data/final/all_results.csv"):
    all_df = pd.read_csv("data/final/all_results.csv")
else:
    all_df = pd.DataFrame({
                    "fixture_id": [],
                    "season": [],
                    "competition": [],
                    "div_type": [],
                    "date_time" : [],
                    "home_team": [],
                    "away_team": [],
                    "home_goals": [],
                    "away_goals": [],
                    "comments" : []
                    })


driver = webdriver.Chrome()

for season, season_id in season_ids.items():
    if season not in seasons_info['scraped'] or season in seasons_info['current_season']:

        # get season result info
        results = scrape_season(season, season_id, driver)

        # transformation
        season_results_list = transform_season(season, results)

        # data types and save as season CSVs
        df = pd.DataFrame(season_results_list)
        df.date_time = pd.to_datetime(df['date_time'], format='%d/%m/%y %H:%M')
        df["fixture_id"] = df["fixture_id"].astype(str)
        df.to_csv(f"data/seasons/{season}_results.csv", index=False)

        if season not in seasons_info['scraped']:
            seasons_info['scraped'].append(season)
            with open("data/raw/seasons_info.json", "w") as f:
                json.dump(seasons_info, f, indent=4)

        # merge updates into final table and split into played/unplayed results
        print(f"merging {season} data")
        merge_seasons(all_df, df)

driver.quit()
