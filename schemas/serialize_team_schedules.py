def serialize_team_schedule(matchup) -> dict:
    return {
        "id": str(matchup["_id"]),
        "team": matchup["team"],
        "matchups": matchup["matchups"]
    }

def serialize_team_schedules(matchup) -> list:
    return [serialize_team_schedule(matchup) for matchup in matchup]