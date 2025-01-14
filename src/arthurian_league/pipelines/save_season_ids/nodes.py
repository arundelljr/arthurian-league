import requests
from bs4 import BeautifulSoup

# Scrape web html
def _get_url_soup(link):
    response = requests.get(link) 
    soup = BeautifulSoup(response.content, "html.parser") # Parse html
    return soup


# Extract season names and corresponding IDs
def _extract_season_ids(soup):
    select_element = soup.find("select", id="form1_selectedSeason") # Find season dropdown menu
    season_elements = select_element.find_all("option") # Select season elements ie. names and IDs
    season_ids = {} # Create empty dictionary
    for element in season_elements:
        season_id = element['value']  # Extract season ID
        season_name = element.text.strip()  # Extract season name
        season_ids[season_name] = season_id  # Configure key:value pairs (name:ID) in dictionary
    print(season_ids)
    return season_ids