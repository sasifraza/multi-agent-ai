# Multi-Agent AI System

An orchestrated AI system where Claude autonomously coordinates multiple specialized agents to complete complex tasks.

## How It Works
User Task (plain English)
↓
Orchestrator (Claude decides)
↓
├── Research Agent   → answers knowledge questions
├── Calculator Agent → evaluates math expressions
└── Writer Agent     → generates structured reports
↓
Combined Final Answer
## Tech Stack
- Python + Anthropic Claude API
- FastAPI REST API
- Docker
- Azure Container Apps
- GitHub Actions CI/CD

## Live API
- Base URL: `https://multi-agent-app.blacksand-4315d904.eastus.azurecontainerapps.io`
- Swagger Docs: `https://multi-agent-app.blacksand-4315d904.eastus.azurecontainerapps.io/docs`

## Example Request
```bash
curl -X POST https://multi-agent-app.blacksand-4315d904.eastus.azurecontainerapps.io/run \
  -H "Content-Type: application/json" \
  -d '{"task": "Research what RAG is, then calculate 2 to the power of 10"}'
```

## Example Response
```json
{
  "task": "Research what RAG is, then calculate 2 to the power of 10",
  "answer": "RAG combines retrieval systems with LLMs... 2^10 = 1024",
  "steps": [
    {"agent": "research_agent", "result": "..."},
    {"agent": "calculator_agent", "result": "..."}
  ]
}
```

## Project Structure

multi-agent-ai/
├── app/
│   ├── agents/
│   │   ├── calculator_agent.py
│   │   ├── research_agent.py
│   │   ├── writer_agent.py
│   │   └── orchestrator.py
│   └── api.py
├── Dockerfile
├── requirements.txt
└── .github/
└── workflows/
└── ci.yml

## Author
Syed Asif Raza, PhD
- GitHub: github.com/sasifraza
- LinkedIn: linkedin.com/in/syed-asif-raza-phd-873aab3