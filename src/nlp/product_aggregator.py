from typing import List, Dict
from sentence_sentiment import analyze_sentences  # import your NLP engine
import os
from review_parser import load_reviews_from_json


def aggregate_product_sentiment(reviews: List[Dict]) -> Dict:
    """
    Aggregates sentiment analysis for a list of reviews belonging to a single product.
    Returns overall sentiment statistics.
    """
    total_polarity = 0
    total_subjectivity = 0
    count = 0

    for review in reviews:
        text = review.get("reviewText", "")  # Safely extract review text
        if not text:
            continue  # Skip empty reviews

        result = analyze_sentences(text)  # Run NLP on the review

        total_polarity += result["summary"]["avg_polarity"]
        total_subjectivity += result["summary"]["avg_subjectivity"]
        count += 1

    if count == 0:
        return {
            "avg_polarity": 0,
            "avg_subjectivity": 0,
            "review_count": 0
        }

    avg_polarity = total_polarity / count
    avg_subjectivity = total_subjectivity / count

    return {
        "avg_polarity": round(avg_polarity, 4),
        "avg_subjectivity": round(avg_subjectivity, 4),
        "review_count": count
    }


if __name__ == "__main__":
    # Dynamically resolve path to data/raw/luxury_beauty_reviews.json
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # /UserIntelligence/src/nlp
    BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))  # /UserIntelligence
    file_path = os.path.join(BASE_DIR, 'data', 'raw', 'luxury_beauty_reviews.json')

    # Debug prints
    print(f"📁 Looking for file at: {file_path}")
    print(f"📁 File exists? {os.path.exists(file_path)}")

    # Load and process reviews
    all_reviews = load_reviews_from_json(file_path)

    # Filter reviews for a single product (use the ASIN of the first one)
    sample_asin = all_reviews[0]['asin']
    product_reviews = [r for r in all_reviews if r['asin'] == sample_asin]

    # Run sentiment aggregation
    result = aggregate_product_sentiment(product_reviews)

    # Print results
    print(f"\n🧴 Product ASIN: {sample_asin}")
    print(f"🔍 Aggregated Sentiment: {result}")