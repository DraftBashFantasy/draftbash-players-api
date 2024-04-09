import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from models.team_schedule import TeamSchedule
from config.database import team_schedules_collection

def fetch_team_schedules():
    nba_teams = {
        'Atlanta Hawks': 'ATL', 'Boston Celtics': 'BOS', 'Brooklyn Nets': 'BKN', 'Charlotte Hornets': 'CHA',
        'Chicago Bulls': 'CHI', 'Cleveland Cavaliers': 'CLE', 'Dallas Mavericks': 'DAL', 'Denver Nuggets': 'DEN',
        'Detroit Pistons': 'DET', 'Golden State Warriors': 'GSW', 'Houston Rockets': 'HOU', 'Indiana Pacers': 'IND',
        'Los Angeles Clippers': 'LAC', 'Los Angeles Lakers': 'LAL', 'Memphis Grizzlies': 'MEM', 'Miami Heat': 'MIA',
        'Milwaukee Bucks': 'MIL', 'Minnesota Timberwolves': 'MIN', 'New Orleans Pelicans': 'NOP', 'New York Knicks': 'NYK',
        'Oklahoma City Thunder': 'OKC', 'Orlando Magic': 'ORL', 'Philadelphia 76ers': 'PHI', 'Phoenix Suns': 'PHX',
        'Portland Trail Blazers': 'POR', 'Sacramento Kings': 'SAC', 'San Antonio Spurs': 'SAS', 'Toronto Raptors': 'TOR',
        'Utah Jazz': 'UTA', 'Washington Wizards': 'WAS',
        'NY': 'NYK', 'GS': 'GSW', 'NO': 'NOP', 'SA': 'SAS', 'PHI': 'PHI', 'BKN': 'BKN', 'CHA': 'CHA', 'CHI': 'CHI',
        'CLE': 'CLE', 'DAL': 'DAL', 'DEN': 'DEN', 'DET': 'DET', 'HOU': 'HOU', 'IND': 'IND', 'LAC': 'LAC', 'LAL': 'LAL',
        'MEM': 'MEM', 'MIA': 'MIA', 'MIL': 'MIL', 'MIN': 'MIN', 'OKC': 'OKC', 'ORL': 'ORL', 'PHO': 'PHX', 'POR': 'POR',
        'SAC': 'SAC', 'TOR': 'TOR', 'UTA': 'UTA', 'WAS': 'WAS', 'ATL': 'ATL', 'BOS': 'BOS', 'GSW': 'GSW', 'NOP': 'NOP',
    }

    month_numbers = {
        'January': '1', 'Febrary': '2', 'March': '3', 'April': '4', 'May': '5', 'June': '6', 'July': '7',
        'August': '8', 'September': '9', 'October': '10', 'November': '11', 'December': '12'
    }

    matchups_response = requests.get('https://hashtagbasketball.com/advanced-nba-schedule-grid')
    soup = BeautifulSoup(matchups_response.text, 'html')
    date_range_text = soup.find('h4').text
    table_rows = soup.find('table').find_all('tr')[2:]

    month_number = month_numbers[date_range_text.split(' ')[2]]
    if len(month_number) < 2:
        month_number = '0'+month_number
    day = int(date_range_text.split(' ')[1])
    year = int(date_range_text.split(' ')[3])

    date = datetime(year, int(month_number), day)

    for row in table_rows:
        row_values = row.find_all('td')
        team = nba_teams[row_values[0].text]
        days = row_values[2:9]
        matchups = []
        for matchup in days:
            if matchup.text != ' ' and matchup.text != '\xa0':
                is_home_game = True
                opponent = matchup.text
                if opponent[0]=='@':
                    is_home_game = False
                    opponent = opponent[1:]
                matchups.append({'date': date.strftime('%Y-%m-%d'), 'opponentTeam': nba_teams[opponent], 'isHomeGame': is_home_game})
            date += timedelta(days=1)

        team_schedule = TeamSchedule(team=team, matchups=matchups)
        team_schedules_collection.update_one(
                                        {"team": dict(team_schedule)["team"]},
                                        {"$set": dict(team_schedule)},
                                        upsert=True
                                    )
        date = datetime(year, int(month_number), day)
