import requests
from bs4 import BeautifulSoup

def get_nba_player_points_rankings():

    response = requests.get(f'https://www.fantasypros.com/nba/rankings/overall.php')
    soup = BeautifulSoup(response.text, 'html')

    player_points_rankings_rows = soup.find(class_='mobile-table').find('tbody').find_all('tr')
    player_points_rankings = []
    for player_points_rankings_row in player_points_rankings_rows:
        values = player_points_rankings_row.find_all('td')
        team = player_points_rankings_row.find('small').text[1:4]
        player_points_rankings.append({
            "firstName": values[1].find('a').text.split(' ')[0],
            "lastName": values[1].find('a').text.split(' ')[1],
            "team": team,
            "pointsRank": int(values[0].text.replace(',', '')),
        })

    return player_points_rankings