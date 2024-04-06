from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.player_gamelogs import player_gamelogs_router
from routes.players import players_router

app = FastAPI(
    title="Draftbash-Players-API",
    description="API for NBA player stats and gamelogs.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate origin or use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Adjust the allowed HTTP methods as needed
    allow_headers=["*"],  # Allow all headers or specify the required headers
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

app.include_router(player_gamelogs_router)
app.include_router(players_router)