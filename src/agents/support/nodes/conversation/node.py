from langchain.chat_models import init_chat_model
from agents.support.state import State
from agents.support.nodes.conversation.tools import tools
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT

llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=1)

llm = llm.bind_tools(tools)

def conversation(state: State):
    new_state: State = {}
    
    history = state["messages"]    
    last_message = history[-1]
    ai_response = llm.invoke([("system", SYSTEM_PROMPT), ("user", last_message.text)])
    new_state["messages"] = [ai_response]
    return new_state