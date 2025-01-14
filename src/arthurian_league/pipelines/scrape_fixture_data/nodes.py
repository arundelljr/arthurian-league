import pandas as pd
import requests
from bs4 import BeautifulSoup
from arthurian_league.pipelines.save_season_ids.nodes import _get_url_soup

# Set up of functions to be used when extracting information from fixture results table

# Explore table
table = soup.find(class_="tbody")

# Find and extract fixture ids
_list = table.find_all()

fixture_ids = []

for fixture in _list:
    if fixture.get('id') is not None:
        ids = fixture.get('id').split("fixture-")[1]
        fixture_ids.append(ids)


def _extract_element(table, secondary_tag, primary_tag="div"):
    data = [] # Create empty list
    _list = table.find_all(primary_tag, class_=secondary_tag) # Find element within soup

    for element in _list:
        fixture_elements = element.text.strip()
        data.append(fixture_elements)
    return data


def _exctract_fixture_data(seasons):
    
    all_data= [] # Create empty list
    
    for season_name, season_id in seasons:
        print(f"Scraping season: {season_name}")  # Print season being scraped
        
        # Use dynamic URL to cycle through seasons
        soup = _get_url_soup(f"https://fulltime.thefa.com/results/1/10000.html?selectedSeason={season_id}&selectedFixtureGroupAgeGroup=0&previousSelectedFixtureGroupAgeGroup=&selectedFixtureGroupKey=&previousSelectedFixtureGroupKey=&selectedDateCode=all&selectedRelatedFixtureOption=2&selectedClub=&previousSelectedClub=&selectedTeam=")
        
        # Find fixture table
        table = soup.find_all("div", class_="tbody")

        for fixture in table:
            fixture_id =
            home_team = "home
            score = _extract_element(table, "score-col")
            
            
        









# Loop through each season and scrape fixture data
def _scrape_fixture_data(seasons):
    
    all_data = [] # Create empty list
    
    for season_id, season_name in seasons.items():
        print(f"Scraping season: {season_name}")  # Print season being scraped
        
        # Use dynamic URLs to cycle through seasons
        soup = _get_url_soup(f"https://fulltime.thefa.com/results/1/10000.html?selectedSeason={season_id}&selectedFixtureGroupAgeGroup=0&previousSelectedFixtureGroupAgeGroup=&selectedFixtureGroupKey=&previousSelectedFixtureGroupKey=&selectedDateCode=all&selectedRelatedFixtureOption=2&selectedClub=&previousSelectedClub=&selectedTeam=") 
        
        # 
        fixtures = soup.find_all("div", class_="tbody")[0].find_all("div", id=lambda x: x and x.startswith("fixture-"))
    
        # Extract competition, date, home team, away team, score for each fixture
        for fixture in fixtures:
            fixture_id = fixture['id'].split("fixture-")[1]
            competition = _extract_html_attribute(fixture, "div", "type-col", "p")
            home_team = _extract_html_attribute(fixture, "div", "home-team-col", "div", "team-name")
            away_team = _extract_html_attribute(fixture, "div", "road-team-col", "div", "team-name")
            date = _extract_html_attribute(fixture, "div", "datetime-col", "span")
            score = _extract_html_attribute(fixture, "div", "score-col")
    
            # Append data, including the season name
            all_data.append([fixture_id, season_name, competition, date, home_team, away_team, score])
            
    # Store data in a pandas DataFrame
    fixtures_df = pd.DataFrame(all_data, columns=["Fixture_ID", "Season", "Competition", "Date", "Home_Team", "Away_Team", "Score"]) 
    return fixtures_df














# Extract 
def _extract_html_attribute(item, tag1, class1, tag2=None, class2=None):
   
    # Find the primary tag and class
    primary_element = item.find(tag1, class_=class1)

    # If a second tag and class are specified, find nested secondary element
    if tag2:
        if class2:
            secondary_element = primary_element.find(tag2, class_=class2)
        else:
            secondary_element = primary_element.find(tag2)
        # Extract from secondary element
        return secondary_element.text.strip()
    # If no second tag or class, extract from the primary element
    return primary_element.text.strip()




def _save_as_csv(df: pd.DataFrame, save_filepath: str):
    df.to_csv(save_filepath)