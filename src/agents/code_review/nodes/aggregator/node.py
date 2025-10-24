from langchain.chat_models import init_chat_model
from agents.code_review.state import State
from agents.code_review.nodes.aggregator.prompt import SYSTEM_PROMPT

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=1)

def aggregator(state: State):
    security_review = state['security_review']
    maintainability_review = state['maintainability_review']
    messages = [
      # debemos usar xml para estructurar mejor la info y que el llm la entienda mejor
        ("system", SYSTEM_PROMPT),
        ("user", f"Synthesize these code review results into a concise summary with key actions: Security review: {security_review} and Maintainability review: {maintainability_review}")
    ]
    response = llm.invoke(messages)
    return {
        'final_review': response.text
    }
