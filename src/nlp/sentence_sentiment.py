from textblob import TextBlob
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_sentences(text: str, min_sentence_length: int = 3) -> Dict[str, Any]:
    """
    Splits text into sentences and returns both sentence-level sentiment analysis
    and a summary with average polarity/subjectivity.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty or None")
    
    try:
        blob = TextBlob(text.strip())
        sentence_results = []
        total_polarity = 0
        total_subjectivity = 0
        count = 0

        for sentence in blob.sentences:
            sentence_text = str(sentence).strip()
            word_count = len(sentence_text.split())
            
            if word_count < min_sentence_length:
                logger.debug(f"Skipping short sentence: '{sentence_text}' ({word_count} words)")
                continue
            
            polarity = round(sentence.sentiment.polarity, 3)
            subjectivity = round(sentence.sentiment.subjectivity, 3)

            sentence_results.append({
                "sentence": sentence_text,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "word_count": word_count
            })

            total_polarity += polarity
            total_subjectivity += subjectivity
            count += 1

        logger.info(f"Analyzed {len(sentence_results)} sentences from text")

        # Return both raw sentences and aggregate summary
        return {
            "sentences": sentence_results,
            "summary": {
                "avg_polarity": round(total_polarity / count, 4) if count else 0,
                "avg_subjectivity": round(total_subjectivity / count, 4) if count else 0
            }
        }

    except Exception as e:
        logger.error(f"Error analyzing sentences: {str(e)}")
        raise

def get_sentiment_summary(sentence_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary statistics from sentence sentiment results.
    
    Args:
        sentence_results (List[Dict[str, Any]]): Results from analyze_sentences()
        
    Returns:
        Dict[str, Any]: Summary statistics including averages and counts
    """
    if not sentence_results:
        return {
            "total_sentences": 0,
            "avg_polarity": 0.0,
            "avg_subjectivity": 0.0,
            "positive_sentences": 0,
            "negative_sentences": 0,
            "neutral_sentences": 0
        }
    
    polarities = [r["polarity"] for r in sentence_results]
    subjectivities = [r["subjectivity"] for r in sentence_results]
    
    positive_count = sum(1 for p in polarities if p > 0.1)
    negative_count = sum(1 for p in polarities if p < -0.1)
    neutral_count = len(polarities) - positive_count - negative_count
    
    return {
        "total_sentences": len(sentence_results),
        "avg_polarity": round(sum(polarities) / len(polarities), 3),
        "avg_subjectivity": round(sum(subjectivities) / len(subjectivities), 3),
        "positive_sentences": positive_count,
        "negative_sentences": negative_count,
        "neutral_sentences": neutral_count
    }

if __name__ == "__main__":
    # Test with sample text
    text = "The packaging was awful. But the cream worked incredibly well. I'm not sure if I'd buy it again though."

    try:
        results = analyze_sentences(text)
        summary = get_sentiment_summary(results)

        print("📊 Sentence Sentiment Analysis Results:\n")
        
        for i, r in enumerate(results, 1):
            sentiment_emoji = "😊" if r['polarity'] > 0.1 else "😞" if r['polarity'] < -0.1 else "😐"
            print(f"{i}. {sentiment_emoji} Sentence: {r['sentence']}")
            print(f"   → Polarity: {r['polarity']}, Subjectivity: {r['subjectivity']} ({r['word_count']} words)\n")
        
        print("📈 Summary Statistics:")
        print(f"   → Total sentences: {summary['total_sentences']}")
        print(f"   → Average polarity: {summary['avg_polarity']}")
        print(f"   → Average subjectivity: {summary['avg_subjectivity']}")
        print(f"   → Positive: {summary['positive_sentences']}, Negative: {summary['negative_sentences']}, Neutral: {summary['neutral_sentences']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")