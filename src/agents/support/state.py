from langgraph.graph import MessagesState

# Estado que incluye información del cliente e items
class State(MessagesState):
    customer_name: str
    customer_age: str
    phone: str