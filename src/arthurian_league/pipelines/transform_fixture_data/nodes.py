import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# Functions for transforming unclean results table

# Remove non-sensical text from score column
def _clean_score(df):
    df['Score'] = df['Score'].astype(str)
    df['Score'] = df['Score'].str.split('\r').str[0].str.strip()
    return df

# Extract home goals and away goals from score column for valid, played games
def _extract_home(f_value):
    hyphen_index = f_value.find("-")
    return f_value[:hyphen_index] if hyphen_index != -1 else None


def _extract_away(f_value):
    hyphen_index = f_value.find("-")
    return f_value[hyphen_index + 1:] if hyphen_index != -1 else None

# Create home and away goals column
def _create_goals_col(df):
    df['Home_goals'] = df['Score'].apply(_extract_home)
    df['Away_goals'] = df['Score'].apply(_extract_away)
    return df

# Create comments column for unplayed games ('Walkover' etc). Returns NaN if valid score is present
def _create_comments(df):
    df['Comments'] = np.where(df['Score'].str.contains(r'\d', na=False), np.nan, df['Score'])
    return df

# Group column creation functions
def _create_columns(df):
    _create_goals_col(df)
    _create_comments(df)
    return df

# Drop redundant score column
def _drop_col(df):
    df.drop('Score', axis=1, inplace=True)
    return df


# Convert data types
def _convert_to_datetime(df):
    # Convert Date to pandas datetime type
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    return df


def _convert_to_int(df): 
    df['Home_goals'] = pd.to_numeric(df['Home_goals'], errors='coerce')
    df['Away_goals'] = pd.to_numeric(df['Away_goals'], errors='coerce')
    df['Home_goals'] = df['Home_goals'].astype('Int64')
    df['Away_goals'] = df['Away_goals'].astype('Int64')
    return df

# Group datatype conversion functions
def _convert_datatypes(df):
    _convert_to_datetime(df)
    _convert_to_int(df)
    return df

# Create separate dataframes for typical and atypical results and remove respective redundant columns
def _split_fixtures(df):
    results_other = df.dropna(subset=['Comments'])
    results_other = results_other.drop(['Home_goals', 'Away_goals'], axis=1)
    results_normal = df.dropna(subset=['Home_goals'])
    results_normal = results_normal.drop('Comments', axis=1)
    return results_other, results_normal 
