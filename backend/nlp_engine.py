import json
from pathlib import Path
from textblob import TextBlob
from collections import Counter
import re

# Input & output paths
INPUT_PATH = Path("data/processed/sample_reviews.json")
OUTPUT_PATH = Path("backend/processed_product_insights.json")

def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())

def analyze_reviews(reviews):
    polarities = []
    subjectivities = []
    all_noun_phrases = []
    all_words = []

    for review in reviews:
        blob = TextBlob(review)
        polarities.append(blob.sentiment.polarity)
        subjectivities.append(blob.sentiment.subjectivity)
        all_noun_phrases.extend(blob.noun_phrases)
        all_words.extend(clean_text(review).split())

    avg_polarity = sum(polarities) / len(polarities)
    avg_subjectivity = sum(subjectivities) / len(subjectivities)

    # AI Score
    ai_score = round(5 + (avg_polarity * 4) - (avg_subjectivity * 2), 2)

    # Top keywords
    keyword_counts = Counter(all_noun_phrases)
    top_keywords = [phrase for phrase, _ in keyword_counts.most_common(5)]

    # Simple summary sentence generator
    summary = "Reviews are mostly positive." if avg_polarity > 0.2 else (
              "Reviews are mixed." if avg_polarity > -0.2 else
              "Reviews are mostly negative.")
    
    if top_keywords:
        summary += f" Users often mention {', '.join(top_keywords[:2])}."

    return {
        "summary_sentence": summary,
        "ai_score": ai_score,
        "top_keywords": top_keywords
    }

def process_all_products():
    with INPUT_PATH.open("r") as f:
        product_data = json.load(f)

    result = []
    for asin, reviews in product_data.items():
        insights = analyze_reviews(reviews)
        result.append({
            "asin": asin,
            **insights
        })

    with OUTPUT_PATH.open("w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ NLP output saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    process_all_products()