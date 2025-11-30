from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import RESULTS_URL

"""
Logic do not scrape season if scraped and not current season
EXTRA : Then in current season, only scrape fixtures not in fixture IDs (not needed to allow previosuly scraped results to be updated)
"""

def scrape_season(season, season_id, driver):

    url = RESULTS_URL.format(season_id=season_id)
    print(f"fetching {season}")
    driver.get(url)

    print("Waiting...")

    # Wait for a specific element that appears *after* captcha verification
    try:
        table_element = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.results-table-2"))
        )
        print("Table found! Scraping…")
    except TimeoutError:
        print("Timed out waiting for the table.")
        driver.quit()
        exit()

    # Now extract HTML and scrape with BeautifulSoup if you want
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find('div', class_="results-table-2").find('div', class_='tbody').find_all('div', class_="")

    print(f"{season} html fetched")

    return results
