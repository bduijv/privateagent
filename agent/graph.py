import os
from  typing import TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from tools.filesystem import list_files
from tools.executor import execute_command

MODEL= "qwen2.5:7b"
OLLAMA_HOST = os.getenv(
    "OLLAMA_BASE_URL",
    "http://ollama:11434",
)

#Register the tools available to the model:
tools = [list_files, execute_command]

llm = ChatOllama(
    model=MODEL,
    base_url=OLLAMA_HOST,
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)


def call_model(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])

    print("MODEL RESPONSE:", response)
    print("TOOL CALLS:", response.tool_calls)

    return {
        "messages": [response]
    }

def build_graph():
    graph = StateGraph(MessagesState)

    graph.add_node("call_model", call_model)
    graph.add_node("tools", ToolNode(tools))

    graph.add_edge(START,"call_model")

    graph.add_conditional_edges(
        "call_model",
        tools_condition,
    )

    graph.add_edge("tools", "call_model")

    return graph.compile()
