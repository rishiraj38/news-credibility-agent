"""
Clean Gradio UI for News Credibility Analyzer.
"""

import gradio as gr
import json
from agent.graph import run_analysis


def analyze(input_text: str):
    """Analyze article and return results."""
    if not input_text or not input_text.strip():
        return "Error", 0, json.dumps({"error": "No input provided"}, indent=2)

    try:
        is_url = input_text.strip().startswith("http")
        report = run_analysis(input_text, article_url=input_text if is_url else None)

        verdict = report.get("verdict", {})
        
        # Check for errors in the report
        if "Failed to extract content from URL" in str(report):
            return "Extraction Error", 0, json.dumps(report, indent=2)

        return (
            verdict.get("credibility", "Unknown"),
            verdict.get("confidence_score", 0),
            json.dumps(report, indent=2)
        )

    except Exception as e:
        print(f"Error: {e}")
        return "Error", 0, json.dumps({"error": str(e)}, indent=2)


def create_ui():
    """Create a premium, minimalist Gradio UI interface."""
    from config.settings import get_llm_config
    llm_conf = get_llm_config()
    model_name = llm_conf.get("model", "Llama-3 (Local)")
    
    # Industrial Flat Theme CSS (No Gradients)
    custom_css = """
    .gradio-container {
        background-color: #0d1117 !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #c9d1d9 !important;
    }
    .main-header {
        border-bottom: 1px solid #30363d !important;
        margin-bottom: 2rem !important;
        padding-bottom: 1rem !important;
    }
    h1 { 
        color: #58a6ff !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }
    .flat-card {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
    }
    .sidebar-info {
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
        padding: 1rem !important;
    }
    .primary-btn {
        background-color: #238636 !important;
        border: 1px solid #2ea043 !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    .primary-btn:hover { background-color: #2ea043 !important; }
    """

    with gr.Blocks(title="Veritas AI", css=custom_css) as demo:
        with gr.Sidebar(elem_classes="sidebar-info"):
            gr.Markdown("### ⚙️ System Status")
            gr.Markdown(f"**Model:** `{model_name}`")
            gr.Markdown("**Backend:** `LangGraph Agent`")
            gr.Markdown("**RAG Index:** `FAISS (Cosine)`")
            gr.Markdown("---")
            gr.Markdown("### 🛠️ Information")
            gr.Markdown("Veritas AI uses semantic analysis and retrieval-augmented generation to verify news claims in real-time.")

        with gr.Column(elem_classes="main-header"):
            gr.Markdown("# 🛡️ Veritas AI", elem_id="header")
            gr.Markdown("Minimalist News Credibility Engine")
        
        with gr.Row():
            with gr.Column(scale=3, elem_classes="flat-card"):
                article_input = gr.Textbox(
                    label="📝 News Input (URL or Text)",
                    placeholder="Paste article here...",
                    lines=12
                )
                analyze_btn = gr.Button("Analyze Credibility", variant="primary", elem_classes="primary-btn")

            with gr.Column(scale=2):
                with gr.Column(elem_classes="flat-card"):
                    gr.Markdown("### 📊 Analysis Results")
                    cred_output = gr.Label(label="Credibility Score")
                    conf_output = gr.Number(label="Confidence Level (%)")
                
                with gr.Accordion("🔍 Technical Trace", open=False):
                    full_report = gr.Code(label="Agent State JSON", language="json", lines=10)

        analyze_btn.click(
            fn=analyze,
            inputs=[article_input],
            outputs=[cred_output, conf_output, full_report]
        )

        gr.Markdown(
            "<center style='color: #8b949e; font-size: 0.8rem; margin-top: 3rem;'>"
            "Capstone Project Milestone 2 | Optimized for Reliability"
            "</center>"
        )

    return demo


def launch():
    """Launch the UI interface."""
    print("\n🚀 Starting Veritas AI Minimalist UI...")
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    launch()
