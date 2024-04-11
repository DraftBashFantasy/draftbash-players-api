from datetime import date, timedelta
import pandas as pd
import numpy as np
from config.database import player_gamelogs_collection, players_collection
from schemas.serialize_player_gamelogs import serialize_player_gamelogs
from schemas.serialize_players import serialize_players

def fetch_weekly_projections():
    current_date = pd.to_datetime(date.today())
    players_gamelogs = serialize_player_gamelogs(player_gamelogs_collection.find())

    gamelogs_df = pd.json_normalize(players_gamelogs)

    # Select and reorder columns
    gamelogs_df = gamelogs_df[['season', 'date', 'playerId', 'team', 'opponentTeam', 'isStarter', 
            'minutesPlayed', 'fieldGoalsAttempted', 'fieldGoalsMade', 'freeThrowsAttempted', 
            'freeThrowsMade', 'threesAttempted', 'threesMade', 'points', 'steals', 'blocks', 
            'assists', 'rebounds', 'turnovers', 'position']]
    gamelogs_df['date'] = pd.to_datetime(gamelogs_df['date'])
    gamelogs_df = gamelogs_df[gamelogs_df['minutesPlayed'] > 0]

    players = serialize_players(players_collection.find())

    players_df = pd.json_normalize(players)
    players_df = players_df[['playerId', 'depthChartOrder', 'position', 'team.abbreviation', 'injuryStatus']]
    players_df['isStarter'] = players_df['depthChartOrder'].apply(lambda x: x==1)

    players_avg_df = pd.DataFrame(columns=['playerId', 'isStarter', 'team', 'isStarter', 'position',
                                    'injuryStatus', 'avgFieldGoalsAttempted', 'avgFieldGoalsMade', 
                                'avgThreesMade', 'avgPoints', 'avgSteals', 'avgBlocks', 
                                'avgAssists', 'avgRebounds', 'avgTurnovers',
                                'avgFreeThrowsAttempted', 'avgFreeThrowsMade'])

    for key, row in players_df.iterrows():
        prev_gms = gamelogs_df[(gamelogs_df['date'] < current_date) & (gamelogs_df['playerId'] == row['playerId'])]

        # The stats whose weighted averages will be taken.
        stats = {'fieldGoalsAttempted': None, 'fieldGoalsMade': 
                None, 'threesMade': None, 'points': None, 'steals': None, 'blocks': None,
                'assists': None, 'rebounds': None, 'turnovers': None,
                'freeThrowsAttempted': None, 'freeThrowsMade': None}
            
        for stat in stats.keys():
            if len(prev_gms) == 0 and row['isStarter']==True:
                stats[stat] = gamelogs_df[
                    (gamelogs_df['date'] < current_date) & 
                    (gamelogs_df['isStarter']==True) & 
                    (gamelogs_df['position']==row['position'])
                ][stat].mean()
            elif len(prev_gms) == 0 and row['isStarter']==False:
                stats[stat] = gamelogs_df[(gamelogs_df['date'] < current_date) & (gamelogs_df['isStarter']==False) & (gamelogs_df['position']==row['position'])][stat].mean()
            elif prev_gms.tail(15)['isStarter'].sum() == 0 and row['isStarter']==True:
                stats[stat] = gamelogs_df[(gamelogs_df['date'] < current_date) & (gamelogs_df['isStarter']==1) & (gamelogs_df['position']==row['position'])][stat].mean() 
            elif prev_gms.tail(5)['isStarter'].sum() == 1 and row['isStarter']==0:
                # If the player has started the last 5 games and is now returning to a bench role,
                # they should be expected to get the stats they averaged as a bench player
                player_bench_games = gamelogs_df[(gamelogs_df['date'] < pd.to_datetime(date.today())) & (gamelogs_df['isStarter']==False) & (gamelogs_df['playerId']==row['playerId'])]
                if len(player_bench_games) < 3:
                    stats[stat] = gamelogs_df[(gamelogs_df['date'] < pd.to_datetime(date.today())) & (gamelogs_df['isStarter']==False) & (gamelogs_df['position']==row['position'])][stat].mean()
                else:
                    stats[stat] = player_bench_games[stat].mean()
            else:
                weights = .98 ** ((current_date - prev_gms['date']).dt.days)
                weighted_sum = np.sum(weights * prev_gms[stat])
                weights_sum = np.sum(weights)
                if weights_sum > 0:
                    weighted_avg = weighted_sum / weights_sum
                    stats[stat] = weighted_avg
                    
        avg_stats = {f"avg{stat[0].upper()+stat[1:]}": value for stat, value in stats.items()}   
        avg_stats['playerId'] = row['playerId']
        avg_stats['isStarter'] = row['isStarter']
        avg_stats['position'] = row['position']
        avg_stats['injuryStatus'] = row['injuryStatus']
        avg_stats['team'] = row['team.abbreviation']
        players_avg_df.loc[len(players_avg_df)] = avg_stats

    players_avg_df