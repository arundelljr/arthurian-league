import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from kedro_datasets.json import JSONDataset
from arthurian_league.pipelines.save_season_ids.nodes import _get_url_soup


def _extract_html_attribute(loop_item, html_tag1, html_class1, html_tag2=None, html_class2=None):
   # Find the primary tag and class
    primary_element = loop_item.find(html_tag1, class_=html_class1)

    # If a second tag is specified, find it inside the primary element
    if html_tag2:
        if html_class2:
            secondary_element = primary_element.find(html_tag2, class_=html_class2)
        else:
            secondary_element = primary_element.find(html_tag2)
        return secondary_element.text.strip()
    # If no second tag, extract from the primary element
    return primary_element.text.strip()


# Loop through each season and scrape data
def _scrape_fixture_data(seasons):
    all_data = []
    for season_id, season_name in seasons.items():
        print(f"Scraping season: {season_name}")  # Print season being scraped
    
        soup = _get_url_soup(f"https://fulltime.thefa.com/results/1/10000.html?selectedSeason={season_id}&selectedFixtureGroupAgeGroup=0&previousSelectedFixtureGroupAgeGroup=&selectedFixtureGroupKey=&previousSelectedFixtureGroupKey=&selectedDateCode=all&selectedRelatedFixtureOption=2&selectedClub=&previousSelectedClub=&selectedTeam=")
        
        # Find all fixtures inside the 'tbody' class
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

def _save_as_csv(df: pd.DataFrame, save_filepath: str):
    df.to_csv(save_filepath)