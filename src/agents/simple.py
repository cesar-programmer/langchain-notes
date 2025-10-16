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
    items: List[str]

def node_1(state: State) -> State:
    # Inicializar datos del cliente si no existen
    new_state: State = {}
    
    if state.get("customer_name") is None:
        new_state["customer_name"] = "Cesar"
        new_state["customer_age"] = 25
        new_state["items"] = ["laptop", "mouse"]
    
    # Crear system prompt que usa la información del estado
    system_prompt = f"""
    Eres un asistente de ventas. 
    Cliente: {new_state.get('customer_name', state.get('customer_name'))}
    Edad: {new_state.get('customer_age', state.get('customer_age'))}
    Items en carrito: {new_state.get('items', state.get('items', []))}
    
    Saluda al cliente por su nombre y menciona los items en su carrito.
    """
    
    # Crear mensajes incluyendo el system prompt
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Hola, quiero información sobre mis productos")
    ]
    
    # El LLM procesa los mensajes con la información del estado
    ai_response = llm.invoke(messages)
    
    # Guardar la conversación en el estado
    new_state["messages"] = messages + [ai_response]
    
    print(f"Cliente: {new_state.get('customer_name', state.get('customer_name'))}")
    print(f"Items: {new_state.get('items', state.get('items'))}")
    print(f"Respuesta IA: {ai_response.content}")
    
    return new_state

# Construir el grafo
builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()
