import requests
import csv
from pathlib import Path

# URLs for high-quality fact-checking datasets
DATASETS = {
    "covid_fact_checks.csv": "https://raw.githubusercontent.com/diptamath/covid_fake_news/main/data/Constraint_Train.csv",
    # Add more if needed
}

def ingest():
    raw_dir = Path(__file__).parent.parent / "rag" / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, url in DATASETS.items():
        print(f"📥 Downloading {filename} from {url}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            target_path = raw_dir / filename
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            # Count rows
            with open(target_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = sum(1 for row in reader) - 1
                
            print(f"   ✅ Success! Saved {rows} fact-checks to {target_path}")
        except Exception as e:
            print(f"   ⚠️ Failed to download {filename}: {e}")

if __name__ == "__main__":
    ingest()
