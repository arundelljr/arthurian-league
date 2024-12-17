import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from arthurian_league.pipelines.scrape_fixture_data.nodes import _save_as_csv

# Cleaning node
def _clean_score(df):
    df['Score'] = df['Score'].astype(str)
    df['Score'] = df['Score'].str.split('\r').str[0].str.strip()
    return df

# Create columns node
def _extract_home(f_value):
    hyphen_index = f_value.find("-")
    return f_value[:hyphen_index] if hyphen_index != -1 else None


def _extract_away(f_value):
    hyphen_index = f_value.find("-")
    return f_value[hyphen_index + 1:] if hyphen_index != -1 else None


def _create_goals_col(df):
    df['Home_goals'] = df['Score'].apply(_extract_home)
    df['Away_goals'] = df['Score'].apply(_extract_away)
    return df


def _create_comments(df):
    df['Comments'] = np.where(df['Score'].str.contains(r'\d', na=False), np.nan, df['Score'])
    return df


def _create_columns(df):
    _create_goals_col(df)
    _create_comments(df)
    return df

# Drop columns node
def _drop_col(df):
    df.drop('Score', axis=1, inplace=True)
    return df


# Convert data types node
def _convert_to_datetime(df):
    # Convert Date to pandas datetime type
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    return df

# Create Comments column for descriptions of atypical results from Score column
# Convert Homegoals and Awaygoals to numeric type (nulls for descriptive entries) and then to Int64
# Drop Score column
# Check datatypes


def _convert_to_int(df): 
    df['Home_goals'] = pd.to_numeric(df['Home_goals'], errors='coerce')
    df['Away_goals'] = pd.to_numeric(df['Away_goals'], errors='coerce')
    df['Home_goals'] = df['Home_goals'].astype('Int64')
    df['Away_goals'] = df['Away_goals'].astype('Int64')
    return df


def _convert_datatypes(df):
    _convert_to_datetime(df)
    _convert_to_int(df)
    return df


def _split_fixtures(df):
    # Create separate dataframes for normal and unexpected results and remove respective unwanted columns
    results_other = df.dropna(subset=['Comments'])
    results_other = results_other.drop(['Home_goals', 'Away_goals'], axis=1)
    results_normal = df.dropna(subset=['Home_goals'])
    results_normal = results_normal.drop('Comments', axis=1)
    return results_other, results_normal 

