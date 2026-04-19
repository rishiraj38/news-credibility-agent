import requests
from bs4 import BeautifulSoup
import json
import os

def web_search(query: str, max_results: int = 3) -> list[dict]:
    """
    Perform a simple web search using DuckDuckGo HTML (no API key required).
    Returns a list of results with title, link, and snippet.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # We use DuckDuckGo's HTML version for simple scraping
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for i, result in enumerate(soup.find_all('div', class_='result')):
            if i >= max_results:
                break
                
            title_tag = result.find('a', class_='result__a')
            snippet_tag = result.find('a', class_='result__snippet')
            
            if title_tag and snippet_tag:
                results.append({
                    "claim": query,
                    "verdict": "Web Search Result",
                    "evidence": snippet_tag.get_text().strip(),
                    "source": title_tag['href'],
                    "title": title_tag.get_text().strip()
                })
        
        return results
    except Exception as e:
        print(f"   ⚠️ Web search failed: {e}")
        return []

def format_search_result(result: dict) -> str:
    """Format a web search result for RAG use."""
    return f"""Claim: {result['claim']}
Verdict: Unverified (Web Result)
Evidence: {result['evidence']}
Source: {result['source']}"""
