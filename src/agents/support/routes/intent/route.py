from pydantic import BaseModel, Field
from typing import Literal
from langchain.chat_models import init_chat_model
from agents.support.state import State
from agents.support.routes.intent.prompt import SYSTEM_PROMPT

# este es el esquema de salida esperado del modelo de lenguaje para la ruta de intenciones
class RouteIntent(BaseModel):
    step: Literal["conversation", "booking"] = Field(
        'conversation', description="The next step in the routing process"
    )

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=1)
llm = llm.with_structured_output(schema=RouteIntent)

# aqui definimos la funcion de ruta de intenciones que usa el modelo de lenguaje para decidir el siguiente paso
def intent_route(state: State) -> Literal["conversation", "booking"]:
    history = state["messages"]
    print('*'*100)
    print(history)
    print('*'*100)
    # aqui invocamos el modelo de lenguaje con el prompt del sistema y el historial de mensajes
    schema = llm.invoke([("system", SYSTEM_PROMPT)] + history)
    # retornamos la ruta decidida por el modelo de lenguaje
    if schema.step is not None:
        return schema.step
    return 'conversation'