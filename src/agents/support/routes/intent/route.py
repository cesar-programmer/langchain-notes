from pydantic import BaseModel, Field
from typing import Literal
from langchain.chat_models import init_chat_model
from agents.support.state import State
from agents.support.routes.intent.prompt import SYSTEM_PROMPT

from agents.support.utils.utils import clean_history_for_llm 

class RouteIntent(BaseModel):
    step: Literal["conversation", "booking"] = Field(
        'conversation',  # Este es el valor default (argumento posicional 0)
        description="The next step in the routing process"  # Este es un keyword argument
    )

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=1)
llm = llm.with_structured_output(schema=RouteIntent)


def intent_route(state: State) -> Literal["conversation", "booking"]:
    
    # *** LA SOLUCIÓN LIMPIA ***
    # Limpia el historial con tu nueva función
    filtered_history = clean_history_for_llm(state["messages"])
    
    print('*'*100)
    print("HISTORIAL FILTRADO (LIMPIO):", filtered_history)
    print('*'*100)

    # Invoca el LLM solo con el historial limpio
    schema = llm.invoke([("system", SYSTEM_PROMPT)] + filtered_history)
    
    if schema.step is not None:
        return schema.step
    return 'conversation'