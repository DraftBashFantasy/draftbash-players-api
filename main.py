from fastapi import FastAPI

# Define the app
app = FastAPI(
    title="MyApp",
    description="Hello API developer!",
    version="0.1.0"
)

#Define the APIs
@app.get("/")
async def main():
    return {"message": "Hello World"}