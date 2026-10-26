import os
from  typing import TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

MODEL= "qwen2.5-coder:7b"
OLLAMA_HOST = os.getenv(
    "OLLAMA_BASE_URL",
    "http://ollama:11434",
)

# Define the state passed through the graph:
class AgentState(TypedDict):
    prompt: str
    response: str

# Configure the language model:
llm = ChatOllama(
    model=MODEL,
    base_url=OLLAMA_HOST,
    temperature=0,
)

# Define a graph node:
def call_model(state:AgentState) -> dict:
    result = llm.invoke(state["prompt"])

    return {
        "response": str(result.content),
    }

# build the graph:
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("call_model", call_model)

    graph.add_edge(START,"call_model")
    graph.add_edge("call_model", END)

    return graph.compile()

# Run the graph:
def main():
    app = build_graph()

    result = app.invoke(
        {
            "prompt": (
                "You are a local coding assistant. "
                "Briefly introduce yourself and explain "
                "that you can help with python projects."
            )
        }
    )

    print(f"Model: {MODEL}")
    print(f"Ollama: {OLLAMA_HOST}")
    print()
    print(result["response"])

if __name__ == "__main__":
    main()
