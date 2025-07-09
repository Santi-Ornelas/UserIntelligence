import json
from pathlib import Path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.nlp.sentiment import analyze_sentiment

def load_reviews_from_dataset(filepath: str, max_reviews: int = 10) -> list:
    """
    Load and parse reviews from the Luxury Beauty dataset.
    Returns a list of reviews: user, rating, comment
    """
    reviews = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                review = {
                    "user": data.get("reviewerID", "unknown_user"),
                    "rating": data.get("overall", None),
                    "comment": data.get("reviewText", "")
                }
                reviews.append(review)
                if len(reviews) >= max_reviews:
                    break
        print(f"[INFO] Loaded {len(reviews)} reviews from dataset.")
        return reviews

    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}")
        return []

if __name__ == "__main__":
    file_path = Path("data/raw/luxury_beauty_reviews.json")
    reviews = load_reviews_from_dataset(file_path, max_reviews=5)

    for r in reviews:
        sentiment = analyze_sentiment(r["comment"])
        print(f"👤 {r['user']} | ⭐ {r['rating']} | 💬 {r['comment']}")
        print(f"   → Polarity: {sentiment['polarity']}, Subjectivity: {sentiment['subjectivity']}\n")