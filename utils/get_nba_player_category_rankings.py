import requests
from bs4 import BeautifulSoup

def get_nba_player_category_rankings():

    player_category_rankings_response = requests.get(f'https://www.fantasypros.com/nba/rankings/overall.php')
    soup = BeautifulSoup(player_category_rankings_response.text, 'html')

    player_categories_rankings_rows = soup.find(class_='mobile-table').find('tbody').find_all('tr')
    player_categories_rankings = []
    for player_categories_rankings_row in player_categories_rankings_rows:
        values = player_categories_rankings_row.find_all('td')
        team = player_categories_rankings_row.find('small').text[1:4]
        player_categories_rankings.append({
            "firstName": values[1].find('a').text.split(' ')[0],
            "lastName": values[1].find('a').text.split(' ')[1],
            "categoryRank": int(values[0].text.replace(',', '')),
            "team": team
        })

    return player_categories_rankings