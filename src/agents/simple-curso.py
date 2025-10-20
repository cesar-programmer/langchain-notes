from pyexpat.errors import messages
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
import random

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=1)

# Estado que incluye información del cliente e items
class State(MessagesState):
    customer_name: str
    customer_age: int

def node_1(state: State):
    new_state: State = {}
    
    if state.get("customer_name") is None:
        new_state["customer_name"] = "Cesar"
    else:
        new_state["customer_age"] = random.randint(18, 65)
    
    history = state["messages"]    
    ai_response = llm.invoke(history)
    new_state["messages"] = [ai_response]
    return new_state

# Construir el grafo
builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()
