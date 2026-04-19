# Step 7 - research_agent.py
import anthropic

KNOWLEDGE = {
    "machine learning": "ML is a subset of AI that enables systems to learn from data.",
    "deep learning": "Deep learning uses neural networks with many layers to learn patterns.",
    "rag": "RAG combines retrieval systems with LLMs to answer questions from documents.",
    "agentic ai": "Agentic AI systems autonomously plan and execute tasks using tools.",
    "python": "Python is a high-level programming language popular in AI and data science.",
}

def research_agent(query: str) -> str:
    client = anthropic.Anthropic()
    
    # Find relevant knowledge
    context = ""
    for key, value in KNOWLEDGE.items():
        if key in query.lower():
            context += f"{value}\n"
    
    if not context:
        context = "No specific knowledge found. Answer based on general knowledge."

    messages = [{
        "role": "user",
        "content": f"Context: {context}\n\nQuestion: {query}\n\nAnswer concisely."
    }]

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=messages
    )
    return response.content[0].text