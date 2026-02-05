"""
Streamlit Sentiment Analysis App
--------------------------------
This application:
• Accepts JSON input containing review dictionary
• Performs sentiment analysis using VADER
• Outputs sentiment results in JSON format
• Displays summary counts
• Handles invalid input gracefully
"""

import streamlit as st
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# -----------------------------------
# Initialize Sentiment Analyzer
# -----------------------------------
analyzer = SentimentIntensityAnalyzer()


# -----------------------------------
# Function: Classify Sentiment
# -----------------------------------
def classify_sentiment(text):
    """
    Classifies sentiment using VADER compound score.
    """

    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"


# -----------------------------------
# Function: Analyze Reviews
# -----------------------------------
def analyze_reviews(review_dict):
    """
    Processes review dictionary and returns structured JSON output.
    """

    sentiments = {}

    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for review_id, review_text in review_dict.items():

        # Handle empty review
        if not review_text or not review_text.strip():
            sentiments[review_id] = "neutral"
            neutral_count += 1
            continue

        sentiment = classify_sentiment(review_text)

        sentiments[review_id] = sentiment

        if sentiment == "positive":
            positive_count += 1
        elif sentiment == "negative":
            negative_count += 1
        else:
            neutral_count += 1

    output = {
        "sentiments": sentiments,
        "summary": {
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count
        }
    }

    return output


# -----------------------------------
# Streamlit UI
# -----------------------------------

st.title("📊 Sentiment Analysis JSON App")

st.write("Upload a JSON file containing review dictionary.")

uploaded_file = st.file_uploader("Upload JSON File", type=["json"])


# -----------------------------------
# File Processing
# -----------------------------------
if uploaded_file is not None:

    try:
        data = json.load(uploaded_file)

        # Validate structure
        if "reviews" not in data:
            st.error("❌ JSON must contain 'reviews' key.")

        elif not isinstance(data["reviews"], dict):
            st.error("❌ 'reviews' must be a dictionary with id:text format.")

        elif len(data["reviews"]) == 0:
            st.warning("⚠ Review dictionary is empty.")

        else:
            output = analyze_reviews(data["reviews"])

            # -------- Summary Metrics --------
            st.subheader("📌 Sentiment Summary")

            summary = output["summary"]

            col1, col2, col3 = st.columns(3)

            col1.metric("Positive", summary["positive_count"])
            col2.metric("Negative", summary["negative_count"])
            col3.metric("Neutral", summary["neutral_count"])

            # -------- JSON Output --------
            st.subheader("📄 Output JSON")
            st.json(output)

            # -------- Download Button --------
            st.download_button(
                label="⬇ Download Output JSON",
                data=json.dumps(output, indent=4),
                file_name="sentiment_results.json",
                mime="application/json"
            )

    except json.JSONDecodeError:
        st.error("❌ Invalid JSON file format.")

    except Exception as e:
        st.error(f"⚠ Unexpected Error: {str(e)}")


# -----------------------------------
# Example Input Section
# -----------------------------------
st.markdown("---")
st.markdown("### 📘 Example Input JSON")

st.code("""
{
  "reviews": {
    "id1": "I love this product!",
    "id2": "Average service",
    "id3": "Very bad experience"
  }
}
""")