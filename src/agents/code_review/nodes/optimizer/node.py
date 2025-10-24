from pydantic import BaseModel, Field
from agents.code_review.state import State
from langchain.chat_models import init_chat_model
from agents.code_review.nodes.optimizer.prompt import SYSTEM_PROMPT

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=1)

class OptimizerReview(BaseModel):
    improvements: list[str] = Field(description="The suggested improvements for the code", default=None)
    optimizedCode: str = Field(description="The optimized version of the code", default=None)

def optimizer_review(state: State):
    code = state['code']
    messages = [
        ("system", SYSTEM_PROMPT),
        ("user", f"Review this code: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(OptimizerReview)
    schema = llm_with_structured_output.invoke(messages)
    return {
        'optimizer_review': schema
    }
