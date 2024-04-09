import requests
from bs4 import BeautifulSoup

def get_nba_player_season_projections():

    player_season_projections_response = requests.get(f'https://www.fantasypros.com/nba/projections/overall.php')
    soup = BeautifulSoup(player_season_projections_response.text, 'html')

    player_projections_rows = soup.find(class_='mobile-table').find('tbody').find_all('tr')
    player_projections = []
    for player_projections_row in player_projections_rows:
        values = player_projections_row.find_all('td')
        player_projections.append({
            "firstName": values[0].find('a').text.split(' ')[0],
            "lastName": values[0].find('a').text.split(' ')[1],
            "points": int(values[1].text.replace(',', '')),
            "rebounds": int(values[2].text.replace(',', '')),
            "assists": int(values[3].text.replace(',', '')),
            "blocks": int(values[4].text.replace(',', '')),
            "steals": int(values[5].text.replace(',', '')),
            "fieldGoalPercentage": float(values[6].text),
            "freeThrowPercentage": float(values[7].text),
            "threesMade": int(values[8].text.replace(',', '')),
            "gamesPlayed": int(values[9].text.replace(',', '')),
            "minutes": int(values[10].text.replace(',', '')),
            "turnovers": int(values[11].text.replace(',', '')),
            "team": values[0].find('small').text[1:4]
        })
    return player_projections