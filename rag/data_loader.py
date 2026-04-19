"""
Sample fact-check dataset for RAG retrieval.
Contains verified claims from reputable fact-checking sources.
"""


# List of words that indicate low-quality/junk content in evidence
JUNK_PHRASES = [
    "log in to continue", "javascript is disabled", "cookies", "sign up", 
    "join facebook", "detected that javascript", "browser", "please wait"
]

def load_external_data() -> list[dict]:
    """Load fact-checks from all CSV and TSV files in the data/raw directory."""
    import csv
    from pathlib import Path
    
    raw_dir = Path(__file__).parent / "data" / "raw"
    if not raw_dir.exists():
        return []
        
    all_data = []
    
    # Process all CSV and TSV files in the directory
    for file_path in raw_dir.glob("*.[ct]sv"):
        is_tsv = file_path.suffix == ".tsv"
        print(f"📄 Loading data from {file_path.name}...")
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                # Determine delimiter
                delim = '\t' if is_tsv else ','
                
                # Check if file has headers by looking at the first line
                first_line = f.readline()
                f.seek(0)
                
                has_header = True
                if is_tsv and ".json" in first_line: # Heuristic for LIAR dataset
                    has_header = False
                
                if has_header:
                    reader = csv.DictReader(f, delimiter=delim)
                    count = 0
                    for row in reader:
                        # Flexible mapping for different dataset formats
                        claim = row.get("claim") or row.get("tweet") or row.get("title") or row.get("text") or ""
                        claim = claim.strip()
                        
                        if not claim or len(claim) < 15:
                            continue
                            
                        evidence = row.get("evidence") or row.get("abstract") or row.get("content") or ""
                        evidence = evidence.strip()
                        
                        if any(phrase in evidence.lower() for phrase in JUNK_PHRASES):
                            continue
                        
                        verdict = row.get("verdict") or row.get("label") or "Unverified"
                        source = row.get("source") or row.get("fact_check_url") or row.get("news_url") or file_path.name
                        category = row.get("category") or "general"
                        
                        all_data.append(process_row(claim, verdict, evidence, source, category))
                        count += 1
                        if count >= 2000: break
                else:
                    # Handle headerless files (like LIAR dataset TSVs)
                    reader = csv.reader(f, delimiter=delim)
                    count = 0
                    for row in reader:
                        if len(row) < 3: continue
                        
                        # LIAR format: ID, Label, Claim, Category, Speaker...
                        verdict = row[1]
                        claim = row[2]
                        category = row[3] if len(row) > 3 else "general"
                        source = row[4] if len(row) > 4 else file_path.name
                        evidence = f"Statement by {source}. Context: {row[13] if len(row) > 13 else 'No additional context'}"
                        
                        all_data.append(process_row(claim, verdict, evidence, source, category))
                        count += 1
                        if count >= 2000: break
                        
                print(f"   ✓ Loaded {count} rows from {file_path.name}")
        except Exception as e:
            print(f"   ⚠️ Error loading {file_path.name}: {e}")
            
    return all_data

def process_row(claim, verdict, evidence, source, category):
    """Normalize row data for internal use."""
    verdict_lower = str(verdict).lower()
    if verdict_lower in ['real', 'true', 'supported', 'mostly-true', 'half-true']:
        verdict_norm = "Supported"
    elif verdict_lower in ['fake', 'false', 'contradicted', 'misleading', 'pants-fire', 'barely-true']:
        verdict_norm = "Contradicted"
    else:
        verdict_norm = "Unverified"
        
    return {
        "claim": claim,
        "verdict": verdict_norm,
        "evidence": (evidence or "No detailed evidence provided.")[:500],
        "source": source,
        "category": category
    }

def get_fact_check_data() -> list[dict]:
    """Return the merged fact-check database (external data only)."""
    return load_external_data()


def get_fact_check_by_category(category: str = None) -> list[dict]:
    """Get fact-check data filtered by category."""
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
    """Get all unique categories in the database."""
    all_data = get_fact_check_data()
    categories = set(item.get("category", "general") for item in all_data)
    return sorted(list(categories))
