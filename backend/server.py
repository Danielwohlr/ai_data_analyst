from fastapi import FastAPI, Request
from app.agents.tools import orchestratorAgent

app = FastAPI()

@app.get("/")
def read_root():
    name = "Jesse Sorsa"
    result = orchestratorAgent(name)
    return {"message": f"{result}"}


@app.post("/orchestrate")
async def run_orchestrator(request: Request):
    body = await request.json()  # Parse raw JSON into a Python dict
    name = body.get("name", "World")  # Safely access "name" key
    result = orchestratorAgent(name)
    return {"message": f"This is the result, {result}!"}
    