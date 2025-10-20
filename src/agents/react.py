from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from langchain_core.tools import tool
import requests
from typing import Optional

@tool("get_products", description="Get the products that the store offers and filter by price.")
def get_products(price: Optional[int] = None):
	response = requests.get("https://api.escuelajs.co/api/v1/products")
	products = response.json()

	return "".join([f"{product['title']} - ${product['price']}" for product in products])


@tool("get_weather", description="Get the weather of a city")
def get_weather(city: str):
    response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")
    data = response.json()
    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
    data = response.json()
    response = f"The weather in {city} is {data["current_weather"]["temperature"]}C with {data["current_weather"]["windspeed"]}km/h of wind."
    return response

tools_list = [get_products, get_weather]

system_prompt = """
Eres un asistente de ventas que ayuda a los clientes a encontrar los productos que necesitan y dar el clima de la ciudad

Tus tools son:
- get_products: para obtener los productos que ofreces en la tienda
- get_weather: para obtener el clima de la ciudad
"""
messages = [
    ("system", system_prompt),
    ("user", "Dime los productos que ofreces en la tienda")
]
llm = init_chat_model("gemini-2.5-pro",model_provider="google_genai", temperature=0)

agent = create_agent(
    model=llm,
    tools=tools_list,
    system_prompt=system_prompt,
)
