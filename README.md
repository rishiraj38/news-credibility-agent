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

## 🌟 Overview

Misinformation spreads rapidly across digital platforms, making manual fact-checking nearly impossible. **Veritas AI** tackles this challenge by employing a robust **Agentic RAG Framework**. Rather than relying on a static knowledge base, the system actively queries a local FAISS vector store filled with 7,500+ verified fact-checks. If a claim is novel or missing from the local database, the agent intelligently falls back to a **Live Web Search** to retrieve the latest real-time context before making a credibility assessment.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- A valid [Groq API Key](https://console.groq.com/keys) (Free tier is sufficient)

### Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/rishiraj38/news-credibility-agent.git
cd news-credibility-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup API Keys
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Running the Application

```bash
python app.py
```
The application will launch locally on `http://0.0.0.0:7860`.

---

## 🎯 Key Features & Deliverables Achieved

This project fulfills all required criteria for the Agentic AI Misinformation Monitoring milestone:

1. **Agentic Framework (LangGraph)**: The system utilizes `LangGraph` to manage a deterministic 4-step workflow: `Input → Analyze → Fact Check → Report`.
2. **Explicit State Management**: State is strictly managed using Python `TypedDict` (`AgentState`), tracking variables like claims, risk flags, and retrieval results across graph nodes.
3. **Massive RAG Integration**: Semantic retrieval is implemented using a local FAISS index, powered by a massive dataset of over **7,500 verified fact-checks** (combining the LIAR dataset and the Constraint COVID-19 dataset).
4. **Live Web Search Fallback**: If the FAISS index yields no high-confidence matches, the agent dynamically routes the query to DuckDuckGo, pulling real-time web results to verify breaking news.
5. **Hallucination Mitigation**: The LLM prompts are aggressively constrained (e.g., forcing single-word verdicts like "Supported", "Contradicted", or "Unverified") and instructed to prioritize conservative risk scoring.
6. **Structured Output Reports**: The agent generates a comprehensive UI report containing:
   - **Summary**: Article overview & Risk Factors.
   - **Analysis**: Cross-source verification results (Local RAG vs Web Search).
   - **Verdict**: Dynamic credibility assessment (High/Medium/Low) and Confidence %.

---

## 🧠 Architecture & Agent Workflow

The agentic loop is defined in `agent/graph.py` and operates in a sequential, deterministic manner:

1. **Input Node**: Accepts a URL or raw text. If a URL is provided, it uses `utils/url_loader.py` to scrape the article content (bypassing paywalls/bot-checks when possible) and adds it to the state.
2. **Analysis Node**: Uses an LLM to read the text and extract verifiable claims and risk factors (e.g., sensational language, anonymous sources).
3. **Fact-Check Node**: 
   - **Step A**: The RAG engine embeds the claims and queries the FAISS index. 
   - **Step B**: If local similarity scores are too low, the agent executes a live web search.
   - The best evidence is then passed to the LLM to verify if the evidence Supports, Contradicts, or leaves the claim Unverified.
4. **Report Node**: Dynamically calculates credibility based on the evidence. If evidence contradicts the claims, credibility is **Low**. If supported, it is **High**. If unverified, the system analyzes the extracted risk factors to determine the final score, ensuring robust evaluation even for novel articles.

---

## 📊 Datasets Used

To ensure high-quality RAG retrieval, we utilize a unified dataset:
- **LIAR Dataset**: A benchmark dataset for fake news detection, containing historically verified political and public figures' statements.
- **Constraint COVID-19 Fake News Dataset**: Thousands of fact-checked claims specifically targeting health misinformation and pandemic rumors.

*Note: The datasets are dynamically loaded using `rag/data_loader.py` which unifies CSV and TSV formats, cleans junk data, and normalizes verdicts.*

---

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
│   ├── data_loader.py   # Loads and formats the local fact-check datasets (TSV/CSV)
│   └── data/raw/        # Raw dataset files (e.g., valid.tsv, covid_fact_checks.csv)
├── app/
│   └── ui.py          # Modern Gradio Web Interface
├── utils/
│   ├── search.py      # Live web search fallback (DuckDuckGo integration)
│   ├── ingest_data.py # Automated dataset downloading
│   └── url_loader.py  # Web scraper for extracting text from URLs
├── config/
│   └── settings.py    # Environment variables and thresholds
└── app.py             # Application entry point
```

---

## 🧪 Testing

To test for a **High Credibility / High Confidence** result, input an article that is strictly factual and lacks emotional language. 

**Example High Credibility Input:**
> "The James Webb Space Telescope recently captured new images of the Orion Nebula. The data reveals previously unseen star-forming regions and planetary disks. According to researchers at NASA, these observations will help refine our understanding of stellar evolution. The telescope uses infrared instruments to peer through dense cosmic dust."

**Example Low Credibility / Misinformation Input:**
> "Breaking: The new virus variant is actually caused by 5G towers. The government is trying to hide this by forcing everyone to stay indoors. A secret insider report confirmed that the towers emit radiation that alters human DNA!"
