import json
from typing import List, Dict, Any


def load_reviews_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Loads and parses review data from an Amazon line-delimited JSON file.
    Returns a list of cleaned review dictionaries.
    """
    reviews = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)

                review_text = data.get("reviewText", "").strip()
                summary = data.get("summary", "").strip()
                overall = data.get("overall", None)
                asin = data.get("asin", "").strip()
                reviewer_id = data.get("reviewerID", "").strip()

                if review_text and summary and overall and asin:
                    reviews.append({
                    "asin": asin,
                    "reviewerID": reviewer_id,
                    "summary": summary,
                    "reviewText": review_text,
                    "overall": overall
                    })

            except json.JSONDecodeError:
                continue  # Skip malformed lines

    return reviews