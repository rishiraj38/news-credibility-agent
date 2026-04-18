"""
Article analysis functions - claims, risks, and report generation.
"""

import json
import re
from langchain_groq import ChatGroq
from config.settings import get_llm_config


def analyze_article(article_text: str) -> tuple[list, list, float]:
    """
    Extract claims and detect risk factors from article.

    Returns: (claims, risk_flags, risk_score)
    """
    config = get_llm_config()

    if not config.get("api_key"):
        return _simple_analysis(article_text)

    try:
        llm = ChatGroq(api_key=config["api_key"], model=config["model"], temperature=0.1)

        # Combined analysis prompt
        prompt = f"""Analyze this article and extract:
1. Key factual claims (statements that can be verified)
2. Risk factors (emotional language, lack of sources, bias, sensationalism)

Article:
{article_text[:5000]}

Respond in JSON format:
{{
    "claims": ["claim 1", "claim 2"],
    "risk_flags": ["flag 1", "flag 2"],
    "risk_score": 0.3
}}

IMPORTANT: If the text is a factual, scientific, or neutral news report, you MUST output an empty list `[]` for risk_flags and keep risk_score exactly 0.0. Do not invent risk factors if none exist. Keep risk_score low (0.0-0.4) unless article is clearly clickbait or conspiracy."""

        response = llm.invoke([("human", prompt)])
        result = _parse_json_response(response.content)

        claims = result.get("claims", [])
        risk_flags = result.get("risk_flags", [])
        risk_score = float(result.get("risk_score", 0.3))

        return claims[:5], risk_flags, min(risk_score, 1.0)

    except Exception as e:
        print(f"LLM analysis failed: {e}")
        return _simple_analysis(article_text)


def _simple_analysis(article_text: str) -> tuple[list, list, float]:
    """Simple pattern-based analysis without LLM."""
    # Extract sentences as claims
    sentences = re.split(r'[.!?]+', article_text)
    claims = [s.strip() for s in sentences if 20 < len(s.strip()) < 200]

    # Detect risk patterns - be conservative
    risk_flags = []
    risk_score = 0.1  # Start with low base score

    text_lower = article_text.lower()

    # Only flag if multiple emotional words
    emotional_words = ["shocking", "incredible", "miracle", "scandal", "outrageous", "exposed"]
    count = sum(1 for w in emotional_words if w in text_lower)
    if count >= 3:
        risk_flags.append("Sensational language detected")
        risk_score += 0.2

    # Anonymous sources
    if "anonymous" in text_lower or "unnamed" in text_lower:
        risk_flags.append("Anonymous sources used")
        risk_score += 0.15

    # Absolute claims
    if re.search(r'\b(always|never|everyone|no one)\b', text_lower):
        risk_flags.append("Absolute/definitive claims")
        risk_score += 0.15

    return claims[:5], risk_flags, min(risk_score, 1.0)


def fact_check(claim: str, retrieved_docs: list) -> dict:
    """Verify a single claim against retrieved evidence."""
    config = get_llm_config()

    if not retrieved_docs:
        return {
            "claim": claim,
            "verification": "Unverified",
            "evidence": "No relevant fact-checks found in database."
        }

    if not config.get("api_key"):
        # Simple keyword matching
        doc_text = retrieved_docs[0]["document"].lower()
        if "contradicted" in doc_text or "false" in doc_text:
            return {"claim": claim, "verification": "Contradicted", "evidence": retrieved_docs[0]["document"][:300]}
        elif "supported" in doc_text:
            return {"claim": claim, "verification": "Supported", "evidence": retrieved_docs[0]["document"][:300]}
        return {"claim": claim, "verification": "Unverified", "evidence": retrieved_docs[0]["document"][:300]}

    try:
        llm = ChatGroq(api_key=config["api_key"], model=config["model"], temperature=0.1)

        evidence_text = "\n".join([doc["document"] for doc in retrieved_docs])

        prompt = f"""Verify this claim against the evidence:

Claim: {claim}

Evidence:
{evidence_text[:1000]}

Respond with one word: Supported, Contradicted, or Unverified"""

        response = llm.invoke([("human", prompt)])
        verification = response.content.strip()

        # Extract just the verdict word
        for v in ["Supported", "Contradicted", "Unverified"]:
            if v in verification:
                return {"claim": claim, "verification": v, "evidence": retrieved_docs[0]["document"][:300]}

        return {"claim": claim, "verification": "Unverified", "evidence": retrieved_docs[0]["document"][:300]}

    except Exception:
        return {"claim": claim, "verification": "Unverified", "evidence": retrieved_docs[0]["document"][:300]}


def generate_report(claims: list, risk_flags: list, verification_results: list, article_text: str) -> dict:
    """Generate the final credibility report."""
    # Calculate credibility - use balanced scoring
    if not verification_results:
        # No verification = Medium (not Low)
        credibility = "Medium"
        confidence = 45
        reasoning = "Claims extracted but no matching fact-checks found in database. This doesn't mean the article is false - it may cover new or niche topics."
    else:
        supported = sum(1 for r in verification_results if r.get("verification") == "Supported")
        contradicted = sum(1 for r in verification_results if r.get("verification") == "Contradicted")
        unverified = sum(1 for r in verification_results if r.get("verification") == "Unverified")
        total = len(verification_results)

        # More nuanced scoring
        if contradicted > 0 and contradicted >= supported:
            credibility = "Low"
            confidence = 60 + min(30, contradicted * 10)
            reasoning = f"{contradicted} of {total} claims contradicted by fact-checking sources."
        elif supported > 0 and supported > contradicted:
            credibility = "High"
            confidence = 65 + min(25, supported * 8)
            reasoning = f"{supported} of {total} claims supported by fact-checking sources."
        elif unverified == total:
            if len(risk_flags) == 0:
                credibility = "Medium"
                confidence = 50
                reasoning = "No claims could be verified against existing fact-checks. The article appears neutral, but we lack data to confirm it."
            else:
                credibility = "Low"
                confidence = 35
                reasoning = "Claims unverified and risk factors detected. Approach with caution."
        else:
            credibility = "Medium"
            confidence = 50
            reasoning = f"Mixed results: {supported} supported, {contradicted} contradicted, {unverified} unverified."

    # Adjust for many risk factors only
    if len(risk_flags) >= 4:
        if credibility == "High":
            credibility = "Medium"
            confidence -= 15
        elif credibility == "Medium":
            confidence -= 10

    confidence = max(20, min(95, confidence))

    # Build report
    return {
        "summary": {
            "article_overview": article_text[:300] + "..." if len(article_text) > 300 else article_text,
            "key_claims": claims[:5],
            "risk_factors": risk_flags[:5]
        },
        "analysis": {
            "fact_check_results": verification_results[:5]
        },
        "verdict": {
            "credibility": credibility,
            "confidence_score": confidence,
            "reasoning": reasoning
        },
        "disclaimer": "This is an AI-generated credibility assessment. Always verify important claims with trusted sources."
    }


def _parse_json_response(text: str) -> dict:
    """Extract JSON from LLM response."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return {"claims": [], "risk_flags": [], "risk_score": 0.3}
