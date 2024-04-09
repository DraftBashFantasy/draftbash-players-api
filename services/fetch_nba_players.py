import requests
from models.player import Player
from config.database import players_collection
from bs4 import BeautifulSoup
from utils.get_nba_player_category_rankings import get_nba_player_category_rankings
from utils.get_nba_player_points_rankings import get_nba_player_points_rankings
from utils.get_nba_player_season_projections import get_nba_player_season_projections
from utils.get_nba_player_season_totals import get_nba_player_season_totals

nba_teams = {
    "ATL": {"name": "Hawks", "location": "Atlanta", "abbreviation": "ATL"},
    "BOS": {"name": "Celtics", "location": "Boston", "abbreviation": "BOS"},
    "BKN": {"name": "Nets", "location": "Brooklyn", "abbreviation": "BKN"},
    "CHA": {"name": "Hornets", "location": "Charlotte", "abbreviation": "CHA"},
    "CHI": {"name": "Bulls", "location": "Chicago", "abbreviation": "CHI"},
    "CLE": {"name": "Cavaliers", "location": "Cleveland", "abbreviation": "CLE"},
    "DAL": {"name": "Mavericks", "location": "Dallas", "abbreviation": "DAL"},
    "DEN": {"name": "Nuggets", "location": "Denver", "abbreviation": "DEN"},
    "DET": {"name": "Pistons", "location": "Detroit", "abbreviation": "DET"},
    "GSW": {"name": "Warriors", "location": "Golden State", "abbreviation": "GSW"},
    "HOU": {"name": "Rockets", "location": "Houston", "abbreviation": "HOU"},
    "IND": {"name": "Pacers", "location": "Indiana", "abbreviation": "IND"},
    "LAC": {"name": "Clippers", "location": "Los Angeles", "abbreviation": "LAC"},
    "LAL": {"name": "Lakers", "location": "Los Angeles", "abbreviation": "LAL"},
    "MEM": {"name": "Grizzlies", "location": "Memphis", "abbreviation": "MEM"},
    "MIA": {"name": "Heat", "location": "Miami", "abbreviation": "MIA"},
    "MIL": {"name": "Bucks", "location": "Milwaukee", "abbreviation": "MIL"},
    "MIN": {"name": "Timberwolves", "location": "Minneapolis", "abbreviation": "MIN"},
    "NOP": {"name": "Pelicans", "location": "New Orleans", "abbreviation": "NOP"},
    "NYK": {"name": "Knicks", "location": "New York", "abbreviation": "NYK"},
    "OKC": {"name": "Thunder", "location": "Oklahoma City", "abbreviation": "OKC"},
    "ORL": {"name": "Magic", "location": "Orlando", "abbreviation": "ORL"},
    "PHI": {"name": "76ers", "location": "Philadelphia", "abbreviation": "PHI"},
    "PHX": {"name": "Suns", "location": "Phoenix", "abbreviation": "PHX"},
    "POR": {"name": "Blazers", "location": "Portland", "abbreviation": "POR"},
    "SAC": {"name": "Kings", "location": "Sacramento", "abbreviation": "SAC"},
    "SAS": {"name": "Spurs", "location": "San Antonio", "abbreviation": "SAS"},
    "TOR": {"name": "Raptors", "location": "Toronto", "abbreviation": "TOR"},
    "UTA": {"name": "Jazz", "location": "Utah", "abbreviation": "UTA"},
    "WAS": {"name": "Wizards", "location": "Washington", "abbreviation": "WAS"}
}

def fetch_nba_players():

    player_categories_rankings = get_nba_player_category_rankings()
    player_points_rankings = get_nba_player_points_rankings()
    player_projections = get_nba_player_season_projections()
    player_totals = get_nba_player_season_totals()
    player_drops_list = requests.get('https://api.sleeper.app/v1/players/nba/trending/drop?limit=50').json()
    player_adds_list = requests.get('https://api.sleeper.app/v1/players/nba/trending/add?limit=50').json()
        
    response = requests.get('https://api.sleeper.app/v1/players/nba')
    for player_id, player_data in response.json().items():
        try:
            if player_data['swish_id']:
                points_rank = None
                category_rank = None
                player_season_projections = None
                team = nba_teams[player_data['team']]
                nba_api_id = None
                seasonTotals = None
                drop_count = None
                add_count = None

                for player_drop in player_drops_list:
                    if player_data['player_id'] == player_drop['player_id']:
                        drop_count = int(player_drop['count'])
                        break

                for player_add in player_adds_list:
                    if player_data['player_id'] == player_add['player_id']:
                        add_count = int(player_add['count'])
                        break
                
                for player_points_ranking in player_points_rankings:
                    if player_data['first_name'] == player_points_ranking['firstName'] and player_data['last_name'] == player_points_ranking['lastName'] and player_data['team'] == player_points_ranking['team']:
                        points_rank = player_points_ranking['pointsRank']
                        break
        
                for player_categories_ranking in player_categories_rankings:
                    if player_data['first_name'] == player_categories_ranking['firstName'] and player_data['last_name'] == player_categories_ranking['lastName'] and player_data['team'] == player_categories_ranking['team']:
                        category_rank = player_categories_ranking['categoryRank']
                        break

                for player_projection in player_projections:
                    if player_data['first_name'] == player_projection['firstName'] and player_data['last_name'] == player_projection['lastName'] and player_data['team'] == player_projection['team']:
                        player_season_projections = {
                            "pointsLeagueRank": points_rank,
                            "categoryLeagueRank": category_rank,
                            "points": player_projection['points'],
                            "rebounds": player_projection['rebounds'],
                            "assists": player_projection['assists'],
                            "steals": player_projection['steals'],
                            "blocks": player_projection['blocks'],
                            "turnovers": player_projection['turnovers'],
                            "fieldGoalPercentage": player_projection['fieldGoalPercentage'],
                            "freeThrowPercentage": player_projection['freeThrowPercentage'],
                            "threesMade": player_projection['threesMade'],
                            "minutes": player_projection['minutes'],
                            "gamesPlayed": player_projection['gamesPlayed']
                        }
                        break

                for player_total in player_totals:
                    nba_api_id = int(player_total[0])
                    first_name = player_total[1].split(' ')[0]
                    last_name = player_total[1].split(' ')[1]
                    team_name = player_total[4]
                    injury_status = player_data['injury_status']
                    if injury_status != None:
                        injury_status = injury_status.upper()

                    if player_data['first_name'] == first_name and player_data['last_name'] == last_name and player_data['team'] == team_name:
                        seasonTotals = {
                            "points": int(player_total[30]),
                            "rebounds": int(player_total[22]),
                            "assists": int(player_total[23]),
                            "steals": int(player_total[25]),
                            "blocks": int(player_total[26]),
                            "turnovers": int(player_total[24]),
                            "fieldGoalPercentage": float(player_total[13]),
                            "freeThrowPercentage": float(player_total[19]),
                            "threesMade": int(player_total[14]),
                            "minutes": int(player_total[10]),
                            "gamesPlayed": int(player_total[6])
                        }
                        break

                player = Player(
                    playerId=player_data['swish_id'],
                    nbaApiPlayerId=nba_api_id,
                    rotowireId=player_data['rotowire_id'],
                    fantasyPositions=player_data['fantasy_positions'],
                    position=player_data['position'],
                    firstName=player_data['first_name'],
                    lastName=player_data['last_name'],
                    height=player_data['height'],
                    weight=player_data['weight'],
                    age=player_data['age'],
                    depthChartOrder=player_data['depth_chart_order'],
                    injuryStatus=injury_status,
                    recentNews=None,
                    fantasyOutlook=None,
                    jerseyNumber=player_data['number'],
                    addCount=add_count,
                    dropCount=drop_count,
                    team=team,
                    seasonProjections=player_season_projections,
                    seasonTotals=seasonTotals
                )

                players_collection.update_one(
                    {"playerId": dict(player)["playerId"]},
                    {"$set": dict(player)},
                    upsert=True
                )
                
        except Exception as e:
            print(e)
