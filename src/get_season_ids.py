import requests
from bs4 import BeautifulSoup
import json
from config import HOME_URL

response = requests.get(HOME_URL)
soup = BeautifulSoup(response.content, "html.parser")

select_element = soup.find('select', id='form1_selectedSeason')
select_season = select_element.find_all('option')

current_season = [select_season[-1].text]

# Add boolean for if scraped yet
season_ids = {season.text : season['value'] for season in select_season}

with open("data/raw/season_ids.json", "w") as f:
    json.dump(season_ids, f, indent=4)

seasons_info = {
    'scraped' : [],
    'current_season' : current_season
    }

with open("data/raw/seasons_info.json", "w") as f:
    json.dump(seasons_info, f, indent=4)
