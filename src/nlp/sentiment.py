from textblob import TextBlob

def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of a given text using TextBlob.
    Returns polarity and subjectivity.
    """
    blob = TextBlob(text)
    return {
        "polarity": round(blob.sentiment.polarity, 3),       # -1 to 1
        "subjectivity": round(blob.sentiment.subjectivity, 3)  # 0 (objective) to 1 (subjective)
    }

if __name__ == "__main__":
    sample = "I absolutely love this product. It’s amazing!"
    result = analyze_sentiment(sample)
    print(f"Text: {sample}")
    print(f"Sentiment → Polarity: {result['polarity']}, Subjectivity: {result['subjectivity']}")
