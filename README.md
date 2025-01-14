# Arthurian League Historical Data Collection

## Project Outline

This project aims to provide a comprehensive and interactive analysis of historical fixtures in the Arthurian League, an amateur 11-a-side football league in London. By scraping and transforming data from the FA website, the project creates a centralized database for historical results and introduces a closeness/excitement rating for each game: 
the Arthurian League Fixture Index Evaluation (ALFIE) rating. 
This is a personal, end-to-end project with the main aim of honing my data engineering and data management skills, as well as data wrangling and analytical techniques. It will also have usable end product for any interested parties (ie. players/admins of the amateur league) such as queryable tables and dashboards.

## Amateur Football

A quick word on how the quirks of an Amateur football league affected some of the thinking behind the project. On creating a fun yet valid rating system, there were a wide range of score lines to cover and many instances of very high scoring, one sided matches. In the professional game, these games still tend to be exciting, however, at this level, they are normally very boring, whether it is due to an inability to put out a competitive XI or a genuine mismatch in the quality of the teams. Therefore the ALFIE rating does not award these high scoring, one sided affairs.
As almost all games are essentially played at ‘Neutral’ venues, the home and away aspect (and respective advantage and disadvantage) is negated. Therefore it made sense when aggregating stats for historic fixtures between two teams to combine games, regardless of whether it was a home fixture or away fixture. This meant creating an aggregated table whereby if you filter by ‘Team A’ vs ‘Team B’, you receive the same aggregated stats as when you filter by ‘Team B’ vs ‘Team A’. This table would then be used in appropriate sections of the dashboard further down the line.





## Project Walkthrough

**1. Data collection**
* Extract season names and respective URL IDs from the league homepage.
* Cycle through different season pages by using formatted URL strings and embedding season IDs 
* Use XML tags to scrape the desired fixture information from the results table.
* Output as CSV file.


**2. Data Cleaning**
* Clean ‘Score’ column by removing nonsensical strings, leaving two types of values: 
  * Final score with hyphen ie. 3 - 1.
  * Descriptive comment of an unplayed game ie. ‘Void’ or ‘Home Walkover’.
* Extract home and away goals of valid games from ‘Score’ column into separate numeric columns, ‘Home goals’ and ‘Away goals’.
* Shift descriptive comments into a new ‘Comments’ column.
* Configure column data types.
* Output three CSV files based on filtering of valid fixtures that can be analysed
  * All - cleaned table with all fixtures
  * Normal - valid fixtures with parsed home and away goals column
  * Other - unplayed fixtures, without a score, containing a comments section 


**3. ALFIE rating**
* A rough rating system was created to award games with low goal differences and high total goals scored whilst shunning one-sided affairs.
* Algorithm was implemented to create ‘ALFIE rating’ column in the ‘Normal’ fixture table 
* Outputs CSV file to be used in downstream analysis and dashboards


**4. Data Aggregation**
* Grouping fixture data by teams whilst negating home and away configuration.
* ‘Normal’ fixture table was copied and the column headers were reversed:
  * ‘Normal’ -     Home Team, Away Team, Home goals, Away goals
  * ‘Reversed’ - Away Team, Home Team, Away goals, Home goals 
* ‘Reversed’ table was stacked underneath the ‘Normal’ table and was Grouped By and Selected For in such a way that achieved the desired effect and avoided duplicates.
* Outputs CSV file to be used in downstream analysis and dashboards

## Further Improvements
1. Build an interactive dashboard for interested parties.
2. Create a historical league table for each division. 
3. Streamline functions
4. Improve data management (ie. dimension tables, avoiding re-scraping fixtures)
5. Implement logging functionality.
