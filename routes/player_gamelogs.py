from fastapi import APIRouter, Path, Query
from models.player_gamelog import PlayerGamelog
from config.database import player_gamelogs_collection
from schemas.serialize_player_gamelogs import serialize_player_gamelogs

player_gamelogs_router = APIRouter()

@player_gamelogs_router.get("/api/v1/players/{player_id}/gamelogs")
async def get_player_gamelogs(player_id: int = Path(..., title="The ID of the player whose gamelogs to retrieve"),
                              season: int = Query(None, title="The season for which to retrieve gamelogs")):

    query_params = {"playerId": player_id}
    if season is not None:
        query_params["season"] = season
    players_gamelogs = serialize_player_gamelogs(player_gamelogs_collection.find(query_params))
    return players_gamelogs

@player_gamelogs_router.post("/api/v1/players/gamelogs")
async def add_player_gamelog(player_gamelog: PlayerGamelog):
    player_gamelogs_collection.update_one(
        {"player_id": dict(player_gamelog)["player_id"], "date": dict(player_gamelog)["date"]},
        {"$set": dict(player_gamelog)},
        upsert=True
    )