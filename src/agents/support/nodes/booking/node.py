from langchain.agents import create_agent
from agents.support.nodes.booking.tools import tools_list
from langchain.chat_models import init_chat_model
from agents.support.nodes.booking.prompt import prompt_template

llm = init_chat_model("gemini-2.5-pro",model_provider="google_genai", temperature=0)

booking_node = create_agent(
    model=llm,
    tools=tools_list,
    system_prompt=prompt_template.format(),
)
