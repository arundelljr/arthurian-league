import requests
from bs4 import BeautifulSoup
import json

# Scrape web html

def _get_url_soup(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html_parser")
    return soup


# Extract the season links and store IDs and names in dictionary/json AND SAVE AS A FILE SO IT CAN BE STORED IN THE DATASET
def _extract_seasons(soup):
    select_element = soup.find("select", id="form1_selectedSeason")
    season_elements = select_element.find_all("option")
    seasons = {}
    for element in season_elements:
        season_id = element['value']  # Extract the season ID
        season_name = element.text.strip()  # Get the season name
        seasons[season_id] = season_name  # Store with ID as key


def _save_to_json(dictionary, filepath):
    #Save json file so that it can be loaded in later 
    with open(filepath, "w") as outfile: 
        json.dump(dictionary, outfile)
        
    
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
def _scrape_season_data(seasons, soup):
    all_data = []
    for season_id, season_name in seasons.items():
        print(f"Scraping season: {season_name}")  # Print season being scraped
    
        soup = _get_url_soup(soup)
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
    return fixtures_df = pd.DataFrame(all_data, columns=["Fixture_ID", "Season", "Competition", "Date", "Home_Team", "Away_Team", "Score"]) 
    
    
  

