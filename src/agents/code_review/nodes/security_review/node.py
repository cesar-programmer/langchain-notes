from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from agents.code_review.state import State
from agents.code_review.nodes.security_review.prompt import SYSTEM_PROMPT
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=1)


class SecurityReview(BaseModel):
    vulnerabilities: list[str] = Field(description="The vulnerabilities in the code", default=None)
    riskLevel: str = Field(description="The risk level of the vulnerabilities", default=None)
    suggestions: list[str] = Field(description="The suggestions for fixing the vulnerabilities", default=None)


def security_review(state: State):
    code = state['code']
    messages = [
        ("system", SYSTEM_PROMPT),
        ("user", f"Review this code: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(SecurityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {
        'security_review': schema
    }