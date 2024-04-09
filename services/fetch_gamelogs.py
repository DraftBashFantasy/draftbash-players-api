from models.player_gamelog import PlayerGamelog
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
from config.database import player_gamelogs_collection
from config.database import players_collection
from schemas.serialize_players import serialize_players
import time

def fetch_gamelogs():
    players = {player['playerId']: player for player in serialize_players(players_collection.find())}

    current_date = date.today()
    current_year = current_date.year
    current_month = current_date.month
    current_season = None

    if current_month >= 10 and current_month <= 12:
        current_season = current_year
    elif current_month >= 1 and current_month <= 4:
        current_season = current_year-1

    game_dates = []
    start_date = current_date - timedelta(days=21)
    end_date = current_date

    current_date = start_date
    while current_date <= end_date:
        game_dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
        if current_date.month == 4 and current_date.day > 10:
            break

    print(game_dates)
    print(current_season)

    for game_date in game_dates:
        time.sleep(.5)
        matchups_response = requests.get(f'https://sportsdata.usatoday.com/basketball/nba/scores?season={current_season}&date={game_date}')
        soup = BeautifulSoup(matchups_response.text, 'html')
        boxscore_btns = soup.find_all(class_='class-ubgFKmr')
        game_ids = [game.find('a').get('href').split('/')[4] for game in boxscore_btns]
        for game_id in game_ids:
            try:
                time.sleep(.6)

                matchup_response = requests.get(f'https://sportsdata.usatoday.com/basketball/nba/scores/{game_id}')
                soup = BeautifulSoup(matchup_response.text, 'html')
                tables = soup.find(class_='class-rsiWjCO').find_all('tbody')
                home_starter_rows = [table.find_all('tr') for table in tables][0]
                away_starter_rows = [table.find_all('tr') for table in tables][1]
                home_bench_player_rows = [table.find_all('tr') for table in tables][2]
                away_bench_player_rows = [table.find_all('tr') for table in tables][3]

                home_team_abbreviation = soup.find(class_='class-77G4-Jb').find_all(class_='class-yNdnxnv')[0].text
                away_team_abbreviation = soup.find(class_='class-77G4-Jb').find_all(class_='class-yNdnxnv')[1].text
                team_abbreviations = {'home': home_team_abbreviation, 'away': away_team_abbreviation}

                player_roles = {
                    'starters': {'home': home_starter_rows, 'away': away_starter_rows}, 
                    'bench_players': {'home': home_bench_player_rows, 'away': away_bench_player_rows}
                }
                for player_role, teams in player_roles.items():
                    started_game = False
                    if player_role=='starters':
                        started_game = True

                    for team in teams.keys():
                        player_team = None
                        opposing_team = None
                        player_team_score = None
                        is_home_game = None
                        opposing_team_score = None

                        if team=='home':
                            player_team = team_abbreviations['home']
                            player_team_score = int(soup.find_all(class_='class-MPFG1-M')[0].text)
                            opposing_team_score = int(soup.find_all(class_='class-MPFG1-M')[1].text)
                            opposing_team = team_abbreviations['away']
                            is_home_game = True
                        else:
                            player_team = team_abbreviations['away']
                            player_team_score = int(soup.find_all(class_='class-MPFG1-M')[1].text)
                            opposing_team_score = int(soup.find_all(class_='class-MPFG1-M')[0].text)
                            opposing_team = team_abbreviations['home']
                            is_home_game = False

                        gamelogs = [player_data.find_all('td') for player_data in player_roles[player_role][team]]
                        for gamelog in gamelogs:
                            player_id = int(gamelog[0].find('a').get('href').split('/')[5])
                            if len(gamelog) == 15:
                                minutes_played = float(gamelog[1].text.split(':')[0]) + float(gamelog[1].text.split(':')[1])/60
                                points_scored = int(gamelog[2].text)
                                threes_made = int(gamelog[4].text.split('-')[0])
                                threes_attempted = int(gamelog[4].text.split('-')[1])
                                fieldgoals_made = int(gamelog[3].text.split('-')[0])
                                fieldgoals_attempted = int(gamelog[3].text.split('-')[1])
                                freethrows_made = float(gamelog[5].text.split('-')[0])
                                freethrows_attempted = float(gamelog[5].text.split('-')[1])
                                offensive_rebounds = int(gamelog[6].text)
                                defensive_rebounds = int(gamelog[7].text)
                                rebounds = int(gamelog[8].text)
                                assists = int(gamelog[9].text)
                                turnovers = int(gamelog[10].text)
                                steals = int(gamelog[11].text)
                                blocks = int(gamelog[12].text)
                                fouls = int(gamelog[13].text)
                                plus_minus = int(gamelog[14].text)
                                position = players[player_id]['position']

                                gamelog = PlayerGamelog(
                                    season=current_season,
                                    date=game_date,
                                    team=player_team,
                                    isHomeGame=is_home_game,
                                    opponentTeam=opposing_team,
                                    playerTeamScore=player_team_score,
                                    opponentTeamScore=opposing_team_score,
                                    playerId=player_id,
                                    position=position,
                                    isStarter=started_game,
                                    minutesPlayed=minutes_played,
                                    points=points_scored,
                                    fieldGoalsMade=fieldgoals_made,
                                    fieldGoalsAttempted=fieldgoals_attempted,
                                    threesMade=threes_made,
                                    threesAttempted=threes_attempted,
                                    freeThrowsMade=freethrows_made,
                                    freeThrowsAttempted=freethrows_attempted,
                                    offensiveRebounds=offensive_rebounds,
                                    defensiveRebounds=defensive_rebounds,
                                    rebounds=rebounds,
                                    assists=assists,
                                    steals=steals,
                                    blocks=blocks,
                                    turnovers=turnovers,
                                    fouls=fouls,
                                    plusMinus=plus_minus
                                )
                                player_gamelogs_collection.update_one(
                                    {"playerId": dict(gamelog)["playerId"], "date": dict(gamelog)["date"]},
                                    {"$set": dict(gamelog)},
                                    upsert=True
                                )
                            else:
                                gamelog = PlayerGamelog(
                                    season=current_season,
                                    date=game_date,
                                    team=player_team,
                                    isHomeGame=is_home_game,
                                    opponentTeam=opposing_team,
                                    playerTeamScore=player_team_score,
                                    opponentTeamScore=opposing_team_score,
                                    playerId=player_id,
                                    position=position,
                                    isStarter=False,
                                    minutesPlayed=0,
                                    points=0,
                                    fieldGoalsMade=0,
                                    fieldGoalsAttempted=0,
                                    threesMade=0,
                                    threesAttempted=0,
                                    freeThrowsMade=0,
                                    freeThrowsAttempted=0,
                                    offensiveRebounds=0,
                                    defensiveRebounds=0,
                                    rebounds=0,
                                    assists=0,
                                    steals=0,
                                    blocks=0,
                                    turnovers=0,
                                    fouls=0,
                                    plusMinus=0
                                )
                                player_gamelogs_collection.update_one(
                                    {"playerId": dict(gamelog)["playerId"], "date": dict(gamelog)["date"]},
                                    {"$set": dict(gamelog)},
                                    upsert=True
                                )
            except Exception as e: 
                print("Error:")
                print(e)