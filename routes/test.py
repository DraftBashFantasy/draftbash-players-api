from fastapi import APIRouter
from config.database import test_collection

test_router = APIRouter()

@test_router.post("/api/v1/test")
async def insert_tests():
    test_collection.insert_one({"name": "Test"})