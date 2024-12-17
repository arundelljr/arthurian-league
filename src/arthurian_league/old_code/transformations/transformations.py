import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

def _clean_score(df, column):
    df[column] = df[column].astype(str)
    df[column] = df[column].str.split('\r').str[0].str.strip()


def _extract_home(f_value):
    hyphen_index = f_value.find("-")
    return f_value[:hyphen_index] if hyphen_index != -1 else None


def _extract_away(f_value):
    hyphen_index = f_value.find("-")
    return f_value[hyphen_index + 1:] if hyphen_index != -1 else None


def _create_goals_col(df, new_col, func):
    df[new_col] = df['Score'].apply(func)
