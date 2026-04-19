# Step 8 - writer_agent.py
import anthropic

def writer_agent(content: str, format: str = "report") -> str:
    client = anthropic.Anthropic()
    messages = [{
        "role": "user",
        "content": f"Write a concise {format} based on this information:\n\n{content}"
    }]

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=messages
    )
    return response.content[0].text