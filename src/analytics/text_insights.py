import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from textblob import TextBlob
import re
import string

nltk.download('stopwords')
nltk.download('punkt')

STOPWORDS = set(stopwords.words('english'))
PUNCTUATION = set(string.punctuation)


def clean_and_tokenize(text: str):
    if not isinstance(text, str):
        return []
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in STOPWORDS and t not in PUNCTUATION and t.isalpha()]
    return tokens


def get_top_words_by_rating(df: pd.DataFrame, n: int = 20):
    print("🔍 Analyzing top words for 1-star and 5-star reviews...")

    one_star_reviews = df[df['overall'] == 1.0]['reviewText'].dropna()
    five_star_reviews = df[df['overall'] == 5.0]['reviewText'].dropna()

    one_tokens = []
    five_tokens = []

    for review in one_star_reviews:
        one_tokens.extend(clean_and_tokenize(review))

    for review in five_star_reviews:
        five_tokens.extend(clean_and_tokenize(review))

    one_counts = Counter(one_tokens).most_common(n)
    five_counts = Counter(five_tokens).most_common(n)

    print("\n❌ Top words in 1-star reviews:")
    print(one_counts)

    print("\n🌟 Top words in 5-star reviews:")
    print(five_counts)

    return {
        '1-star': dict(one_counts),
        '5-star': dict(five_counts)
    }


def plot_word_freqs(freq_dict: dict):
    print("\n📊 Plotting word frequencies...")

    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    for ax, (title, word_freq) in zip(axs, freq_dict.items()):
        words = list(word_freq.keys())
        counts = list(word_freq.values())
        sns.barplot(x=counts, y=words, ax=ax, palette='Blues_r')
        ax.set_title(f"{title} Reviews")
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Word")
    plt.tight_layout()
    plt.show()


def add_sentiment_scores(df: pd.DataFrame):
    print("🧠 Adding sentiment scores with TextBlob...")

    df['polarity'] = df['reviewText'].apply(
        lambda x: TextBlob(x).sentiment.polarity if isinstance(x, str) else None
    )
    df['subjectivity'] = df['reviewText'].apply(
        lambda x: TextBlob(x).sentiment.subjectivity if isinstance(x, str) else None
    )

    print("\n🧾 Sample sentiment output:")
    print(df[['reviewText', 'polarity', 'subjectivity']].head(3))

    return df


if __name__ == "__main__":
    # 🔧 Sample local run
    import os
    import json

    file_path = os.path.join("data", "raw", "luxury_beauty_reviews.json")
    print("📁 Loading data from JSON...")

    cleaned_data = []
    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            try:
                cleaned_data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"⚠️ Skipping line {i}: {e}")

    df = pd.DataFrame(cleaned_data)
    df['reviewText'] = df['reviewText'].fillna("")
    df['reviewTime'] = pd.to_datetime(df['reviewTime'], errors='coerce')

    print(f"✅ Loaded {len(df)} reviews.")

    # Run core text insight analysis
    freqs = get_top_words_by_rating(df)
    plot_word_freqs(freqs)

    df = add_sentiment_scores(df)