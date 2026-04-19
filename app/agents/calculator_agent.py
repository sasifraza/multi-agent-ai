# Step 6 - calculator_agent.py
import anthropic
import math

TOOLS = [{
    "name": "calculator",
    "description": "Evaluate a math expression.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {"type": "string"}
        },
        "required": ["expression"]
    }
}]

def run_calculator(expression: str) -> str:
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed["abs"] = abs
    result = eval(expression, {"__builtins__": {}}, allowed)
    return f"Result: {result}"

def calculator_agent(task: str) -> str:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": task}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return next((b.text for b in response.content if hasattr(b, "text")), "Done.")

        for block in response.content:
            if block.type == "tool_use":
                result = run_calculator(block.input["expression"])
                messages.append({
                    "role": "user",
                    "content": [{"type": "tool_result", "tool_use_id": block.id, "content": result}]
                })