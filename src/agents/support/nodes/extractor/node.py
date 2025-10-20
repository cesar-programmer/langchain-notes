from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.messages import HumanMessage
from agents.support.state import State
from agents.support.nodes.extractor.prompt import prompt_template

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: Optional[str] = Field(default=None, description="The name of the person, if mentioned")
    email: Optional[str] = Field(default=None, description="The email address of the person, if mentioned")
    phone: Optional[str] = Field(default=None, description="The phone number of the person, if mentioned")
    age: Optional[str] = Field(default=None, description="The age of the person, if mentioned")

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0)
llm = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None:
        # Estrategia 1: Solo mensajes humanos para extracción
        human_messages_only = [msg for msg in history if isinstance(msg, HumanMessage)]
        
        prompt = prompt_template.format()
        schema = llm.invoke([("system", prompt)] + human_messages_only)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state