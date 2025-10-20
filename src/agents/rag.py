from pyexpat.errors import messages
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
import random

llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=1)

openai_vector_store_ids = [
  "vs_68f1a1e722508191ba51713db1cbf9a1",
]

file_search_tool = {
  "type": "file_search",
  "vector_store_ids": openai_vector_store_ids,
}

llm = llm.bind_tools([file_search_tool])

# Estado que incluye información del cliente e items
class State(MessagesState):
    customer_name: str
    customer_age: str
    phone: str

from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
	name: str = Field(description="The person's full name")
	phone: str = Field(description="The person's phone number")
	email: str = Field(description="The person's email address")
	age: str = Field(description="The age of the person.")

llm_with_structured_output = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0)
llm_with_structured_output = llm_with_structured_output.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    # aqui va el trigger para ejecutar el extractor solo si no hay nombre de cliente o si el historial es muy largo
    customer_name = state.get("customer_name", None or len(history) > 20)
    new_state: State = {}
    if customer_name is not None:
        schema = llm_with_structured_output.invoke(history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["customer_age"] = schema.age
    return new_state

def conversation(state: State):
    new_state: State = {}
    
    history = state["messages"]    
    last_message = history[-1]
    customer_name = state.get("customer_name", "john doe")
    system_message = f"you are a helpful assistant that can answer questions about the user called {customer_name}."
    ai_response = llm.invoke([("system", system_message), ("user", last_message.text)])
    new_state["messages"] = [ai_response]
    return new_state

# Construir el grafo
builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, "extractor")
builder.add_edge("extractor", "conversation")
builder.add_edge("conversation", END)

agent = builder.compile()
