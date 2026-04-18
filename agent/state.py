"""
Simple state management for the agent workflow.
"""

from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict):
    """Shared state passed between all agent steps."""
    # Input
    article_text: str
    article_url: Optional[str]

    # Analysis results
    claims: List[str]
    risk_flags: List[str]
    risk_score: float

    # RAG retrieval
    retrieved_docs: Dict[str, List[Dict]]

    # Verification
    verification_results: List[Dict]

    # Final report
    final_report: Dict[str, Any]

    # Errors
    errors: List[str]


def create_initial_state(article_text: str, article_url: str = None) -> AgentState:
    """Create initial state for processing."""
    return {
        "article_text": article_text,
        "article_url": article_url,
        "claims": [],
        "risk_flags": [],
        "risk_score": 0.0,
        "retrieved_docs": {},
        "verification_results": [],
        "final_report": {},
        "errors": []
    }
