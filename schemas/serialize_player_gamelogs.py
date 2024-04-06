def serialize_player_gamelog(player_gamelog) -> dict:
    return {
        "id": str(player_gamelog["_id"]),
        "season": player_gamelog["season"],
        "date": player_gamelog["date"],
        "team": player_gamelog["team"],
        "isHomeGame": player_gamelog["isHomeGame"],
        "opponentTeam": player_gamelog["opponentTeam"],
        "playerTeamScore": player_gamelog["playerTeamScore"],
        "opponentTeamScore": player_gamelog["opponentTeamScore"],
        "playerId": player_gamelog["playerId"],
        "position": player_gamelog["position"],
        "isStarter": player_gamelog["isStarter"],
        "minutesPlayed": player_gamelog["minutesPlayed"],
        "points": player_gamelog["points"],
        "fieldGoalsMade": player_gamelog["fieldGoalsMade"],
        "fieldGoalsAttempted": player_gamelog["fieldGoalsAttempted"],
        "threesMade": player_gamelog["threesMade"],
        "threesAttempted": player_gamelog["threesAttempted"],
        "freeThrowsMade": player_gamelog["freeThrowsMade"],
        "freeThrowsAttempted": player_gamelog["freeThrowsAttempted"],
        "offensiveRebounds": player_gamelog["offensiveRebounds"],
        "defensiveRebounds": player_gamelog["defensiveRebounds"],
        "rebounds": player_gamelog["rebounds"],
        "assists": player_gamelog["assists"],
        "steals": player_gamelog["steals"],
        "blocks": player_gamelog["blocks"],
        "turnovers": player_gamelog["turnovers"],
        "fouls": player_gamelog["fouls"],
        "plusMinus": player_gamelog["plusMinus"]
    }

def serialize_player_gamelogs(player_gamelog) -> list:
    return [serialize_player_gamelog(player_gamelog) for player_gamelog in player_gamelog]