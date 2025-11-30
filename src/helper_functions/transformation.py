def transform_season(season, results):

    """
    Function that transforms all result info parsed from ONE season.
    Takes in season string and results bs object
    """
    print(f"parsing {season} info")

    all_results_list = []

    for fixture in results:

        fixture_id = fixture.attrs['id'][len("fixture-"):]

        competition = fixture.find('div', class_="fg-col").text.strip()
        DIV_type = fixture.find('div', class_="type-col").find('a').text.strip()

        date_and_time_list = fixture.find('div', class_="datetime-col").find_all('span')
        date_time = date_and_time_list[0].text.strip() + ' ' + date_and_time_list[1].text.strip()

        # date_and_time = [dt.text.strip() for dt in date_and_time_list]

        home_team = fixture.find('div', class_="home-team-col").text.strip()
        away_team = fixture.find('div', class_="road-team-col").text.strip()

        # Deal with abnormal scores (Voids, Walkovers, Extra Time etc.)

        lines = fixture.find('div', class_="score-col").text.splitlines()
        clean_lines = [line.strip() for line in lines]
        info = [line for line in clean_lines if len(line) > 0]

        # Normal scores
        if len(info) == 1:
            score = info[0].strip()
            comments = None
        else:
            # Games with Extra Time, Pens etc.
            if info[0][0].isdigit():
                score = info[0].strip()
                comments = info[1].strip()
            # Unplayed Games Walkovers, Voids etc.
            else:
                score = info[1].strip()
                comments = info[0].strip()

        home_goals = score.split('-')[0].strip()
        away_goals = score.split('-')[1].strip()


        all_results_list.append({
                "fixture_id": fixture_id,
                "season": season,
                "competition": competition,
                "div_type": DIV_type,
                "date_time" : date_time,
                "home_team": home_team,
                "away_team": away_team,
                "home_goals": home_goals,
                "away_goals": away_goals,
                "comments" : comments
            })

    return all_results_list
