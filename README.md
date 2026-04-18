---
title: News Credibilty Agent
emoji: 😻
colorFrom: pink
colorTo: green
sdk: gradio
sdk_version: 6.12.0
app_file: app.py
pinned: false
---

# 🛡️ Veritas AI: News Credibility Analyzer

An agentic AI misinformation monitoring system built for **Milestone 2: Agentic AI Misinformation Monitoring**. This project autonomously reasons about content, retrieves fact-checking sources, and generates structured credibility reports.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup API Keys
cp .env.example .env
# Edit .env and add your GROQ_API_KEY (Get a free key at https://console.groq.com/keys)

# 3. Run the application
python app.py
```
The application will launch on `http://0.0.0.0:7860`.

## 🎯 Milestone 2 Deliverables Achieved

This project fulfills all required criteria for the Agentic AI Misinformation Monitoring milestone:

1. **Agentic Framework (LangGraph)**: The system utilizes `LangGraph` to manage a deterministic 4-step workflow: `Input → Analyze → Fact Check → Report`.
2. **Explicit State Management**: State is strictly managed using Python `TypedDict` (`AgentState`), tracking variables like claims, risk flags, and retrieval results across graph nodes.
3. **RAG (FAISS + Sentence Transformers)**: Semantic retrieval is implemented using a local FAISS index, which cross-references extracted claims against a database of fact-checked documents.
4. **Hallucination Mitigation Prompts**: The LLM prompts are aggressively constrained (e.g., forcing single-word verdicts like "Supported", "Contradicted", or "Unverified") and instructed to prioritize conservative risk scoring.
5. **Structured Output**: The agent generates a comprehensive report containing:
   - **Summary**: Article overview & Risk Factors.
   - **Analysis**: Cross-source verification results.
   - **Verdict**: Dynamic credibility assessment (High/Medium/Low) and Confidence %.
   - **Disclaimer**: Built-in ethical AI disclaimer.

## 📂 Project Structure

```text
news-credibility-agent/
├── agent/
│   ├── graph.py       # LangGraph workflow orchestrator (the 4 nodes)
│   ├── state.py       # Shared state structure (AgentState)
│   └── analyzer.py    # LLM interaction: Claim extraction, risk detection, report building
├── rag/
│   ├── vector_store.py  # FAISS index and semantic retrieval logic
│   ├── embedder.py      # all-MiniLM-L6-v2 embedding generation
│   └── data_loader.py   # Loads and formats the local fact-check dataset
├── app/
│   └── ui.py          # Minimalist Gradio Web Interface
├── utils/
│   └── url_loader.py  # Web scraper for extracting text from URLs
├── config/
│   └── settings.py    # Environment variables and LLM configurations
├── app.py             # Application entry point
└── requirements.txt   # Cleaned dependencies (Pydantic removed for simplicity)
```

## 🧠 Agent Workflow Explained

1. **Input Node**: Accepts a URL or raw text. If a URL is provided, it uses `utils/url_loader.py` to scrape the article content and add it to the state.
2. **Analysis Node**: Uses an LLM to read the text and extract verifiable claims and risk factors (e.g., sensational language, anonymous sources).
3. **Fact-Check Node**: The RAG engine embeds the claims and queries the FAISS index. The top matches are passed back to the LLM, which strictly verifies if the evidence Supports, Contradicts, or leaves the claim Unverified.
4. **Report Node**: Dynamically calculates credibility. If evidence contradicts the claims, credibility is **Low**. If supported, it is **High**. If unverified (not in database), it falls back to analyzing the risk factors to determine the score, ensuring robust evaluation even for new articles.

## 🧪 Testing

To test for a **High Credibility / High Confidence** result, input an article that is strictly factual and lacks emotional language. 

**Example High Credibility Input:**
> "The James Webb Space Telescope recently captured new images of the Orion Nebula. The data reveals previously unseen star-forming regions and planetary disks. According to researchers at NASA, these observations will help refine our understanding of stellar evolution. The telescope uses infrared instruments to peer through dense cosmic dust."
