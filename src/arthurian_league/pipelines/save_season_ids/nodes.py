import requests
from bs4 import BeautifulSoup
import json
from kedro.io import DataCatalog
from kedro_datasets.json import JSONDataset

# Scrape web html
def _get_url_soup(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


# Extract the season names and corresponding IDs
def _extract_season_ids(soup):
    select_element = soup.find("select", id="form1_selectedSeason")
    season_elements = select_element.find_all("option")
    season_ids = {}
    for element in season_elements:
        season_id = element['value']  # Extract the season ID
        season_name = element.text.strip()  # Get the season name
        season_ids[season_id] = season_name  # Store with ID as key
    print(season_ids)
    return season_ids


# Store season IDs and names in a json file 
def _save_to_json(data, save_filepath):
    dataset = JSONDataset(filepath=save_filepath)
    dataset.save(data)
