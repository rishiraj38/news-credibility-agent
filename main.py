#!/usr/bin/env python3
"""
News Credibility Analysis System

Simple entry point - initializes RAG and launches UI.

Usage:
    python main.py

Set GROQ_API_KEY in .env file or environment.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import GROQ_API_KEY
from rag.vector_store import initialize_vector_store
from app.ui import launch


def main():
    print("=" * 50)
    print("News Credibility Analyzer")
    print("=" * 50)

    if not GROQ_API_KEY:
        print("⚠️ GROQ_API_KEY not set!")
        print("   Get free key: https://console.groq.com/keys")
        print("   Add to .env file")
        print()

    print("Loading fact-check database...")
    vs = initialize_vector_store()
    print(f"✓ {vs.document_count} documents loaded")
    print()

    launch()


if __name__ == "__main__":
    main()
