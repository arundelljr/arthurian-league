import pandas as pd
import numpy as np


def _choose_columns(df):
    
    fixture_df = df[['Fixture_ID','Home_Team', 'Away_Team', 'Home_goals', 'Away_goals', 'ALFIE_rating']]
    return fixture_df
    
    
def _reverse_fixtures(fixture_df):
    
    swapped_df = fixture_df.rename(columns={'Home_Team' : 'Away_Team', 'Away_Team' : 'Home_Team', 'Home_goals' : 'Away_goals', 'Away_goals' : 'Home_goals'})
    return swapped_df


def _stack_fixtures(fixture_df, swapped_df):
    
    stacked_df = pd.concat([fixture_df, swapped_df], ignore_index=True).rename(columns={"Home_Team" : "Team_1", "Away_Team" : "Team_2", "Home_goals" : "Team_1_goals", "Away_goals" : "Team_2_goals"})

    stacked_df['Total_goals'] = stacked_df['Team_1_goals'] + stacked_df['Team_2_goals']
    return stacked_df

    
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


        

