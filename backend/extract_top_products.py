import json
from collections import defaultdict
from pathlib import Path

# === File Paths ===
INPUT_PATH = Path("data/raw/luxury_beauty_reviews.json")
OUTPUT_PATH = Path("data/processed/sample_reviews.json")

def load_reviews(input_path):
    products_reviews = defaultdict(list)
    with input_path.open("r") as f:
        for line in f:
            try:
                review = json.loads(line)
                asin = review.get("asin")
                text = review.get("reviewText")
                if asin and text:
                    products_reviews[asin].append(text.strip())
            except json.JSONDecodeError:
                continue
    return products_reviews

def extract_top_products(products_reviews, top_n=9, max_reviews=50):
    sorted_products = sorted(
        products_reviews.items(), 
        key=lambda x: len(x[1]), 
        reverse=True
    )[:top_n]

    sample_reviews = {
        asin: reviews[:max_reviews] for asin, reviews in sorted_products
    }
    return sample_reviews

def save_cleaned_data(data, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved to {output_path}")

def main():
    print("🔍 Loading review data...")
    products_reviews = load_reviews(INPUT_PATH)

    print("📦 Extracting top 9 products...")
    top_reviews = extract_top_products(products_reviews)

    print("💾 Saving cleaned data...")
    save_cleaned_data(top_reviews, OUTPUT_PATH)

if __name__ == "__main__":
    main()