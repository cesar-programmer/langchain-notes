from typing import TypedDict, Dict, Any

class State(TypedDict):
    code: str
    security_review: Dict[str, Any]
    maintainability_review: Dict[str, Any]
    final_review: str