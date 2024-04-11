import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URL'))

db = client.player_stats_db

player_gamelogs_collection = db['player_gamelogs']
players_collection = db['players']
team_schedules_collection = db['team_schedules']
test_collection = db['test']