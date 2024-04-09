from fastapi import APIRouter
from config.database import team_schedules_collection
from schemas.serialize_team_schedules import serialize_team_schedules

team_schedules_router = APIRouter()

@team_schedules_router.get("/api/v1/team_schedules")
async def get_team_schedules():
    team_schedules = serialize_team_schedules(team_schedules_collection.find())
    return team_schedules