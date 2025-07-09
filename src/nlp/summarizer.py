import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.api.fetch_dataset_reviews import load_reviews_from_dataset
from src.nlp.sentiment import analyze_sentiment

def summarize_sentiments(reviews: list) -> dict:
    """
    Takes a list of reviews (each with 'comment') and returns summary stats.
    """
    sentiments = [analyze_sentiment(r["comment"]) for r in reviews]

    avg_polarity = round(sum(s["polarity"] for s in sentiments) / len(sentiments), 3)
    avg_subjectivity = round(sum(s["subjectivity"] for s in sentiments) / len(sentiments), 3)

    most_positive = max(zip(reviews, sentiments), key=lambda x: x[1]["polarity"])
    most_negative = min(zip(reviews, sentiments), key=lambda x: x[1]["polarity"])

    return {
        "average_polarity": avg_polarity,
        "average_subjectivity": avg_subjectivity,
        "most_positive": most_positive[0],
        "most_negative": most_negative[0],
    }

if __name__ == "__main__":
    reviews = load_reviews_from_dataset(Path("data/raw/luxury_beauty_reviews.json"), max_reviews=15)
    summary = summarize_sentiments(reviews)

    print(f"\n🧠 Summary for {len(reviews)} Reviews")
    print(f"→ Average Polarity: {summary['average_polarity']}")
    print(f"→ Average Subjectivity: {summary['average_subjectivity']}")
    print(f"\n💚 Most Positive Review:\n{summary['most_positive']['comment']}")
    print(f"\n💔 Most Negative Review:\n{summary['most_negative']['comment']}")