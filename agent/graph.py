"""
LangGraph workflow for News Credibility Analysis.

Simple 4-step pipeline:
Input → Analysis → Fact Check → Report
"""

from langgraph.graph import StateGraph, START, END
from agent.state import AgentState, create_initial_state
from agent.analyzer import analyze_article, fact_check, generate_report
from rag.vector_store import get_vector_store
from config.settings import MAX_CLAIMS_TO_ANALYZE


def input_node(state: AgentState) -> AgentState:
    """Process input - handle URL or text."""
    from utils.url_loader import extract_text_from_url

    article_text = state["article_text"]

    # If URL, extract text
    if article_text.startswith("http"):
        print(f"📥 Extracting text from URL...")
        result = extract_text_from_url(article_text)
        if result and "text" in result:
            state["article_text"] = result["text"]
            print(f"   Extracted {len(result['text'])} characters")
        elif result and "error" in result:
            msg = f"Error: {result['error']}"
            state["errors"].append(msg)
            print(f"   ⚠️ {msg}")
        else:
            msg = f"Failed to extract content from URL: {article_text[:50]}..."
            state["errors"].append(msg)
            print(f"   ⚠️ {msg}")

    # Truncate if too long
    if len(state["article_text"]) > 8000:
        state["article_text"] = state["article_text"][:8000]

    return state


def analysis_node(state: AgentState) -> AgentState:
    """Extract claims and analyze risks."""
    article_text = state["article_text"]

    if not article_text or state["errors"]:
        return state

    print("📝 Analyzing article...")
    claims, risk_flags, risk_score = analyze_article(article_text)

    state["claims"] = claims
    state["risk_flags"] = risk_flags
    state["risk_score"] = risk_score

    print(f"   Found {len(claims)} claims, {len(risk_flags)} risk flags")
    return state


def fact_check_node(state: AgentState) -> AgentState:
    """Retrieve evidence and verify claims."""
    claims = state["claims"]

    if not claims or state["errors"]:
        print("⚠️ No claims to fact-check or previous error exist")
        return state

    print("🔍 Retrieving evidence from RAG database...")
    vector_store = get_vector_store()

    retrieved = {}
    results = []

    for i, claim in enumerate(claims[:MAX_CLAIMS_TO_ANALYZE], 1):
        docs = vector_store.retrieve(claim, top_k=2)
        retrieved[claim] = docs

        # Use the dedicated fact_check function for LLM verification
        if docs:
            score = docs[0].get("score", 0)
            print(f"   Claim {i}: Found strong match ({score:.2f} similarity)")
            result = fact_check(claim, docs)
            result["similarity_score"] = score
        else:
            print(f"   Claim {i}: No highly relevant matches found (below threshold)")
            result = {
                "claim": claim,
                "verification": "Unverified",
                "evidence": "No highly relevant fact-checks found in the current database for this specific claim.",
                "similarity_score": 0.0
            }
            
        results.append(result)

    state["retrieved_docs"] = retrieved
    state["verification_results"] = results

    print(f"   Completed fact-checking {len(results)} claims")
    return state


def report_node(state: AgentState) -> AgentState:
    """Generate final credibility report."""
    print("📊 Generating report...")
    report = generate_report(
        claims=state["claims"],
        risk_flags=state["risk_flags"],
        verification_results=state["verification_results"],
        article_text=state["article_text"]
    )

    state["final_report"] = report
    
    # Include errors in report for UI visibility
    if state["errors"]:
        report["errors"] = state["errors"]

    verdict = report.get("verdict", {})
    print(f"   Credibility: {verdict.get('credibility', 'Unknown')} ({verdict.get('confidence_score', 0)}% confidence)")

    return state


def build_graph() -> StateGraph:
    """Build and compile the LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("input", input_node)
    workflow.add_node("analyze", analysis_node)
    workflow.add_node("fact_check", fact_check_node)
    workflow.add_node("report", report_node)

    # Add edges (sequential flow)
    workflow.add_edge(START, "input")
    workflow.add_edge("input", "analyze")
    workflow.add_edge("analyze", "fact_check")
    workflow.add_edge("fact_check", "report")
    workflow.add_edge("report", END)

    return workflow.compile()


def run_analysis(article_text: str, article_url: str = None) -> dict:
    """Run the complete analysis pipeline."""
    graph = build_graph()
    initial_state = create_initial_state(article_text, article_url)

    print("\n" + "=" * 50)
    print("Starting News Credibility Analysis")
    print("=" * 50)

    final_state = graph.invoke(initial_state)

    print("=" * 50)
    print("Analysis Complete")
    print("=" * 50 + "\n")

    return final_state.get("final_report", {})
