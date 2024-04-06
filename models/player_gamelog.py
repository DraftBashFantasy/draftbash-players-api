from pydantic import BaseModel

# A percentile between 0 and 33 would be considered below average, 33 and 66 average, and 66 and 100 above average
class PlayerGamelog(BaseModel):
    season: int
    date: str
    team: str
    isHomeGame: bool
    opponentTeam: str
    playerTeamScore: int
    opponentTeamScore: int
    playerId: int
    position: str
    isStarter: bool
    minutesPlayed: float
    points: int
    fieldGoalsMade: int
    fieldGoalsAttempted: int
    threesMade: int
    threesAttempted: int
    freeThrowsMade: int
    freeThrowsAttempted: int
    offensiveRebounds: int
    defensiveRebounds: int
    rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    fouls: int
    plusMinus: int