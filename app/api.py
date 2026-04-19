# Step 10 - api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agents.orchestrator import orchestrator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Multi Agent AI API",
    description="Orchestrates multiple AI agents to complete complex tasks.",
    version="1.0.0"
)

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    task: str
    answer: str
    steps: list

@app.get("/")
def root():
    return {"status": "running", "message": "Multi Agent AI is live!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/run", response_model=TaskResponse)
def run(request: TaskRequest):
    if not request.task.strip():
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    try:
        result = orchestrator(request.task)
        return TaskResponse(task=request.task, answer=result["answer"], steps=result["steps"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))