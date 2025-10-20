from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI


def get_weather(city: str) -> str:
    """Get weather information for a given city."""
    return f"It's always sunny in {city}!"

# Initialize the Gemini modelt
model = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

agent = create_agent(
    model=model,
    #model='openai:gpt-4o-mini',
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)
