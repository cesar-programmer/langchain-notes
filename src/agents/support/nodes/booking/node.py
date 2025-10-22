# agents/support/nodes/booking/node.py
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, BaseMessage
from agents.support.nodes.booking.tools import tools_list
from agents.support.nodes.booking.prompt import prompt_template
from agents.support.utils.utils import clean_history_for_llm
from agents.support.state import State

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=1)

_agent = create_agent(
    model=llm,
    tools=tools_list,
    system_prompt=prompt_template.format(),
)

def booking_node(state: State) -> State:
    # 1) Limpia el historial
    cleaned_history = clean_history_for_llm(state["messages"])

    # 2) **CRUCIAL**: el agente interno espera {"messages": [...]} (no una lista suelta)
    inner_in = {"messages": cleaned_history}
    inner_out = _agent.invoke(inner_in)

    # 3) Normalizar la salida a {"messages": [...]}
    if isinstance(inner_out, dict) and "messages" in inner_out:
        return {"messages": (inner_out["messages"])}
    elif isinstance(inner_out, list):
        return {"messages": (inner_out)}
    else:
        # p. ej. un AIMessage suelto
        return {"messages": [inner_out]}
