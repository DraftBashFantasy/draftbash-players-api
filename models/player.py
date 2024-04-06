from pydantic import BaseModel
from typing import Optional

# A percentile between 0 and 33 would be considered below average, 33 and 66 average, and 66 and 100 above average
class Player(BaseModel):
    playerId: int
    nbaApiPlayerId: Optional[int]
    rotowireId: Optional[int]
    fantasyPositions: list
    position: str
    firstName: str
    lastName: str
    team: Optional[str]
    height: int
    weight: int
    age: int
    depthChartOrder: Optional[int]
    injuryStatus: Optional[str]
    recentNews: Optional[str]
    fantasyOutlook: Optional[str]
    jerseyNumber: Optional[int]
    team: Optional[dict]
    seasonProjections: Optional[dict]
    seasonTotals: Optional[dict]
    dropCount: Optional[int]
    addCount: Optional[int]
