from textblob import TextBlob

text = "The packaging was awful. But the cream worked incredibly well."
blob = TextBlob(text)

for sentence in blob.sentences:
    print(f"🧾 Sentence: {sentence}")
    print(f"   → Polarity: {sentence.sentiment.polarity}")
    print(f"   → Subjectivity: {sentence.sentiment.subjectivity}")