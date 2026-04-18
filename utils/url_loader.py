import re
import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url: str, timeout: int = 15) -> dict:
    """
    Extract article text and title from URL, following redirect chains.
    """
    if not url.startswith(("http://", "https://")):
        return None

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

        # First request - allow redirects
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()

        # Check for meta refresh redirect
        final_content = response.content
        redirect_url = _get_meta_redirect(final_content)
        
        if redirect_url:
            print(f"   Following meta redirect: {redirect_url[:50]}...")
            response = requests.get(redirect_url, headers=headers, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            final_content = response.content

        soup = BeautifulSoup(final_content, 'lxml')

        # Remove scripts, styles and nav
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        # Get title
        title = soup.find("h1")
        title = title.get_text().strip() if title else soup.title.string if soup.title else "Article"

        # Broaden extraction: Look for content in common news container classes or tags
        # Major news sites often use specific div classes instead of P tags
        potential_containers = soup.find_all(["p", "div"], class_=re.compile(r"article|story|body|_bIDB|content|text", re.I))
        
        # Also get all standard P tags
        p_tags = soup.find_all("p")
        
        all_elements = list(set(potential_containers + p_tags))
        
        text_blocks = []
        for el in all_elements:
            # Get text and clean it
            el_text = el.get_text(separator=' ', strip=True)
            
            # Filter for substantial, unique blocks (usually news content)
            # Avoid short navigational snippets or very long duplicates
            if 80 < len(el_text) < 3000:
                # Check if this text is already mostly contained in our list to avoid duplication
                if not any(el_text[:50] in existing for existing in text_blocks):
                    text_blocks.append(el_text)

        text = "\n\n".join(text_blocks)

        # Final check - if we have almost no text, it failed
        if len(text.strip()) < 200:
            if "news.google.com" in url:
                print("   Google News redirect failed to resolve via static scraping.")
                return {"error": "Google News link detected. These links use complex redirects that are sometimes blocked. Please try pasting the link to the original article directly."}
            print(f"   Content too short ({len(text.strip())} chars). Failed to extract article body.")
            return None

        return {"title": title, "text": text.strip()}

    except Exception as e:
        print(f"URL extraction failed: {e}")
        return None


def _get_meta_redirect(content) -> str:
    """Check for meta-refresh redirect tags."""
    soup = BeautifulSoup(content, 'lxml')
    result = soup.find("meta", attrs={"http-equiv": lambda x: x and x.lower() == "refresh"})
    if result and result.has_attr("content"):
        # content="0; url=https://..."
        m = re.search(r"url=(.*)", result["content"], re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None
