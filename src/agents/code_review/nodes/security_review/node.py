from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from agents.code_review.state import State

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=1)


class SecurityReview(BaseModel):
    vulnerabilities: list[str] = Field(description="The vulnerabilities in the code", default=None)
    riskLevel: str = Field(description="The risk level of the vulnerabilities", default=None)
    suggestions: list[str] = Field(description="The suggestions for fixing the vulnerabilities", default=None)


def security_review(state: State):
    code = state['code']
    # aqui se podria usar un system prompt mas detallado y ponerlo en otra carpeta y solo importarlo
    messages = [
        ("system", "You are an expert in code security. Focus on identifying security vulnerabilities, injection risks, and authentication issues."),
        ("user", f"Review this code: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(SecurityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {
        'security_review': schema
    }