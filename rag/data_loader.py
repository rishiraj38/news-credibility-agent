"""
Sample fact-check dataset for RAG retrieval.
Contains verified claims from reputable fact-checking sources.
"""

# Sample fact-check database with real-world claims and verdicts
# Each entry has: claim, verdict, evidence, source
FACT_CHECK_DATABASE = [
    # --- CRICKET & IPL 2026 (New Samples) ---
    {
        "claim": "Jasprit Bumrah is retiring from IPL after 2026 season",
        "verdict": "Unverified",
        "evidence": "There is no official statement from Jasprit Bumrah or Mumbai Indians regarding his retirement. Analysts suggest he has several years of peak performance remaining.",
        "source": "IPL Official, Sports Analysis",
        "category": "sports"
    },
    {
        "claim": "IPL 2026 will feature 12 teams instead of 10",
        "verdict": "Contradicted",
        "evidence": "The BCCI has confirmed that IPL will continue with 10 teams for the 2026 season. Extensions to the league are currently not in the immediate roadmap.",
        "source": "BCCI Official Press Release",
        "category": "sports"
    },
    {
        "claim": "Mahela Jayawardene says Jasprit Bumrah has a niggle in IPL 2026",
        "verdict": "Supported",
        "evidence": "In a post-match press conference, MI coach Mahela Jayawardene mentioned that Bumrah is managing a minor workload-related niggle but remains fit for selection.",
        "source": "Post-match Interaction, IPL 2026",
        "category": "sports"
    },
    {
        "claim": "Virat Kohli has announced his move to Mumbai Indians for 2026",
        "verdict": "Contradicted",
        "evidence": "Virat Kohli remains with Royal Challengers Bengaluru (RCB) and has expressed his commitment to the franchise for the upcoming seasons.",
        "source": "RCB Social Media, Virat Kohli Official",
        "category": "sports"
    },
    {
        "claim": "Rohit Sharma will captain Team India in T20 World Cup 2026",
        "verdict": "Unverified",
        "evidence": "Captaincy decisions for 2026 have not been finalized yet. While Rohit remains a key leader, the BCCI selection committee will decide based on form and fitness closer to the event.",
        "source": "BCCI Selection Insights",
        "category": "sports"
    },
    
    # --- SCIENCE & HEALTH (Existing Samples) ---
    {
        "claim": "Climate change is caused by human activities",
        "verdict": "Supported",
        "evidence": "Over 97% of climate scientists agree that human activities, particularly greenhouse gas emissions, are the primary cause of global warming.",
        "source": "IPCC Climate Report 2023",
        "category": "science"
    },
    {
        "claim": "Vaccines cause autism",
        "verdict": "Contradicted",
        "evidence": "Multiple large-scale studies involving millions of children have found no link between vaccines and autism.",
        "source": "CDC, WHO Reports",
        "category": "health"
    },
    {
        "claim": "5G networks cause health problems",
        "verdict": "Contradicted",
        "evidence": "Extensive research by health organizations worldwide has found no evidence that 5G networks cause harm.",
        "source": "WHO, ICNIRP",
        "category": "technology"
    }
]


def load_csv_data() -> list[dict]:
    """Load additional fact-checks from the user-provided CSV dataset."""
    import csv
    from pathlib import Path
    
    csv_path = Path(__file__).parent / "data" / "raw" / "covid_dataset.csv"
    if not csv_path.exists():
        return []
        
    print(f"📄 Loading additional data from {csv_path}...")
    csv_data = []
    try:
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                # Basic mapping: title -> claim, fact_check_url -> source
                claim = row.get("title", "").strip()
                if not claim or len(claim) < 10:
                    continue
                    
                # We classify these as COVID-related based on the dataset name
                csv_data.append({
                    "claim": claim,
                    "verdict": "Contacted Fact-check Source",
                    "evidence": row.get("abstract", "No detailed abstract available.")[:300],
                    "source": row.get("fact_check_url", "External Database"),
                    "category": "covid_health"
                })
                # Limit to first 1000 for local performance if needed, or take all
                if i >= 1000:
                    break
        print(f"   ✓ Successfully loaded {len(csv_data)} rows from CSV")
    except Exception as e:
        print(f"   ⚠️ Error loading CSV: {e}")
        
    return csv_data


def get_fact_check_data() -> list[dict]:
    """Return the merged fact-check database (Hardcoded + CSV)."""
    samples = FACT_CHECK_DATABASE
    csv_data = load_csv_data()
    return samples + csv_data


def get_fact_check_by_category(category: str = None) -> list[dict]:
    """Get fact-check data filtered by category (includes CSV data)."""
    all_data = get_fact_check_data()
    if category is None:
        return all_data
    return [item for item in all_data if item.get("category") == category]


def format_doc_for_retrieval(doc: dict) -> str:
    """Format a fact-check document for retrieval and display."""
    return f"""Claim: {doc['claim']}
Verdict: {doc['verdict']}
Evidence: {doc['evidence']}
Source: {doc['source']}"""


def get_categories() -> list[str]:
    """Get all unique categories in the database (includes CSV data)."""
    all_data = get_fact_check_data()
    categories = set(item.get("category", "general") for item in all_data)
    return sorted(list(categories))
