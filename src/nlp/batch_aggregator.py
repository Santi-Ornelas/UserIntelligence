from collections import defaultdict
from typing import List, Dict
from product_aggregator import aggregate_product_sentiment


def aggregate_by_product(reviews: List[Dict]) -> List[Dict]:
    """
    Groups reviews by ASIN and aggregates sentiment for each product.
    """
    asin_map = defaultdict(list)

    for review in reviews:
        asin = review.get("asin", "").strip()
        if asin:  # Ensure asin is not empty
            asin_map[asin].append(review)

    print(f"📊 Found {len(asin_map)} unique products")

    results = []
    for asin, grouped_reviews in asin_map.items():
        sentiment = aggregate_product_sentiment(grouped_reviews)
        results.append({
            "asin": asin,
            **sentiment
        })

    return results


def aggregate_by_reviewer(reviews: List[Dict]) -> List[Dict]:
    """
    Groups reviews by reviewerID and aggregates sentiment across products per user.
    """
    reviewer_map = defaultdict(list)

    for review in reviews:
        reviewer_map[review["reviewerID"]].append(review)

    results = []
    for reviewer_id, grouped_reviews in reviewer_map.items():
        sentiment = aggregate_product_sentiment(grouped_reviews)
        results.append({
            "reviewerID": reviewer_id,
            **sentiment
        })

    return results

if __name__ == "__main__":
    import os
    from review_parser import load_reviews_from_json

    # Build path dynamically
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
    file_path = os.path.join(BASE_DIR, 'data', 'raw', 'luxury_beauty_reviews.json')

    all_reviews = load_reviews_from_json(file_path)
    print(f"🔎 Sample review:", all_reviews[0])
    
    product_results = aggregate_by_product(all_reviews)
    reviewer_results = aggregate_by_reviewer(all_reviews)

    print("\n📦 Top 5 Products:")
    for r in product_results[:5]:
        print(r)

    print("\n👤 Top 5 Reviewers:")
    for r in reviewer_results[:5]:
        print(r)