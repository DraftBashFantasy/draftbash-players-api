from pydantic import BaseModel

class TeamSchedule(BaseModel):
    team: str
    matchups: list[dict]