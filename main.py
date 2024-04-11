import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.player_gamelogs import player_gamelogs_router
from services.fetch_team_schedules import fetch_team_schedules
from services.fetch_gamelogs import fetch_gamelogs
from services.fetch_nba_players import fetch_nba_players
from services.fetch_weekly_projections import fetch_weekly_projections
from routes.players import players_router
from routes.team_schedules import team_schedules_router
from routes.test import test_router
from dotenv import load_dotenv

load_dotenv()
fetch_weekly_projections()

app = FastAPI(
    title="Draftbash-Players-API",
    description="API for NBA player stats and gamelogs.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": 'api'}

@app.get("/ping")
async def main():
    return "Ping successful!"

app.include_router(player_gamelogs_router)
app.include_router(players_router)
app.include_router(team_schedules_router)
app.include_router(test_router)