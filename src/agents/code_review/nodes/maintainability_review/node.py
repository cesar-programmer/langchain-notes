from pydantic import BaseModel, Field
from agents.code_review.state import State
from langchain.chat_models import init_chat_model


llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=1)

class MaintainabilityReview(BaseModel):
    concerns: list[str] = Field(description="The concerns about the code", default=None)
    qualityScore: int = Field(description="The quality score of the code from 1 to 10", default=None, ge=1, le=10)
    recommendations: list[str] = Field(description="The recommendations for improving the code", default=None)


def maintainability_review(state: State):
    code = state['code']
    messages = [
        ("system", "You are an expert in code quality. Focus on code structure, readability, and adherence to best practices."),
        ("user", f"Review this code: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(MaintainabilityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {
        'maintainability_review': schema
    }
