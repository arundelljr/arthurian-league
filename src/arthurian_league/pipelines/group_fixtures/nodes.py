import pandas as pd
import numpy as np

# Functions for negating home and away fixture configurations and then aggregating data by fixtures

# Select relevant columns, leaving out Date and Seasons. Fixture ID is kept for the stacking of fixtures.
def _choose_columns(df):
    
    fixture_df = df[['Fixture_ID','Home_Team', 'Away_Team', 'Home_goals', 'Away_goals', 'ALFIE_rating']]
    return fixture_df
    

# Swap order of column headers so that score line is given in reverse configuration 
def _reverse_fixtures(fixture_df):
    
    swapped_df = fixture_df.rename(columns={'Home_Team' : 'Away_Team', 'Away_Team' : 'Home_Team', 'Home_goals' : 'Away_goals', 'Away_goals' : 'Home_goals'})
    return swapped_df

# Stack the original and reversed table, renaming and neutralising home and away columns whilst adding total goals column
def _stack_fixtures(fixture_df, swapped_df):
    
    stacked_df = pd.concat([fixture_df, swapped_df], ignore_index=True).rename(columns={"Home_Team" : "Team_1", "Away_Team" : "Team_2", "Home_goals" : "Team_1_goals", "Away_goals" : "Team_2_goals"})

    stacked_df['Total_goals'] = stacked_df['Team_1_goals'] + stacked_df['Team_2_goals']
    return stacked_df

# Group By Team 1 v Team 2 and aggregate goals and ALFIE rating. Fixture ID is left out and Total games is added.
# Grouped fixtures will appear twice but will display the same stats just in a reverse configuration which will improve dashboard functionality downstream.    
def _group_fixtures(stacked_df):
    
    df = stacked_df[['Team_1', 'Team_2', 'Team_1_goals', 'Team_2_goals', 'Total_goals', 'ALFIE_rating']]
    grouped_df = df.groupby(['Team_1', 'Team_2']).agg({
        "Team_1_goals": "sum",
        "Team_2_goals": "sum",
        "Total_goals" : "sum",
        "ALFIE_rating": "mean",
        "Team_1" : "count"
    }).rename(columns={"Team_1" : "Total_games"}).reset_index()

    return grouped_df


        

