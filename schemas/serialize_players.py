from models.player import Player

def serialize_player(player: Player) -> dict:
    return {
        "playerId": player["playerId"],
        "nbaApiPlayerId": player["nbaApiPlayerId"],
        "rotowireId": player["rotowireId"],
        "fantasyPositions": player["fantasyPositions"],
        "position": player["position"],
        "firstName": player["firstName"],
        "lastName": player["lastName"],
        "team": player["team"],
        "height": player["height"],
        "weight": player["weight"],
        "age": player["age"],
        "depthChartOrder": player["depthChartOrder"],
        "injuryStatus": player["injuryStatus"],
        "recentNews": player["recentNews"],
        "fantasyOutlook": player["fantasyOutlook"],
        "jerseyNumber": player["jerseyNumber"],
        "team": player["team"],
        "seasonProjections": player["seasonProjections"],
        "seasonTotals": player["seasonTotals"],
        "dropCount": player["dropCount"],
        "addCount": player["addCount"]
    }

def serialize_players(players) -> list:
    return [serialize_player(player) for player in players]