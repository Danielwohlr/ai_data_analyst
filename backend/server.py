from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.agents.orchestrator import orchestratorAgent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # <-- allow all methods (GET, POST, etc)
    allow_headers=["*"],  # <-- allow all headers
)

@app.get("/")
def read_root():
    name = "Jesse Sorsa"
    result = orchestratorAgent(name)
    return {"message": f"{result}"}


@app.post("/input")
async def run_orchestrator(request: Request):
    body = await request.json()  # Parse raw JSON into a Python dict
    input_data = body.get("input")  # Safer access with .get()
    result = await orchestratorAgent(input_data)
    print(f"this is the result before returning to frontend: {result}")
    return result
