# Step 9 - orchestrator.py
import anthropic
import json
from app.agents.calculator_agent import calculator_agent
from app.agents.research_agent import research_agent
from app.agents.writer_agent import writer_agent

TOOLS = [
    {
        "name": "calculator_agent",
        "description": "Use for any math calculations or numerical problems.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "The math task to solve"}
            },
            "required": ["task"]
        }
    },
    {
        "name": "research_agent",
        "description": "Use for researching topics or answering knowledge questions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The topic to research"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "writer_agent",
        "description": "Use for writing reports or summarizing information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Content to write about"},
                "format": {"type": "string", "description": "Format: report, summary, bullet points"}
            },
            "required": ["content"]
        }
    }
]

def run_agent(tool_name: str, tool_input: dict) -> str:
    if tool_name == "calculator_agent":
        return calculator_agent(tool_input["task"])
    elif tool_name == "research_agent":
        return research_agent(tool_input["query"])
    elif tool_name == "writer_agent":
        return writer_agent(tool_input["content"], tool_input.get("format", "report"))
    return "Unknown agent"

def orchestrator(task: str) -> dict:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": task}]
    steps = []

    print(f"\nTask: {task}")
    print("-" * 50)

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2048,
            tools=TOOLS,
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            final = next((b.text for b in response.content if hasattr(b, "text")), "Done.")
            print(f"\n✅ Final Answer: {final}")
            return {"answer": final, "steps": steps}

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"🤖 Orchestrator calls: {block.name}")
                result = run_agent(block.name, block.input)
                print(f"📥 Result: {result[:100]}...")
                steps.append({"agent": block.name, "input": block.input, "result": result})
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "user", "content": tool_results})