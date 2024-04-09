from pydantic import BaseModel
from typing import Optional

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
