from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()

# ---- Auto-response templates ----
POSITIVE_RESPONSES = [
    "Thank you so much for the kind words! We're thrilled you had a great experience — hope to see you again soon. 🙌",
    "This made our day! Thanks for taking the time to share your feedback. 😊",
    "We really appreciate you! Glad we could deliver a great experience for you.",
]

NEGATIVE_RESPONSES = [
    "We're really sorry to hear this. This isn't the experience we want for you — please reach out to our support team so we can make it right.",
    "Thank you for flagging this, and we apologize for the trouble. We're looking into it and would love the chance to fix things for you.",
    "We're sorry this fell short of expectations. Please DM us your order details so we can resolve this quickly.",
]


def generate_response(label):
    if label == "POSITIVE":
        return random.choice(POSITIVE_RESPONSES)
    else:
        return random.choice(NEGATIVE_RESPONSES)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    chunks = [line.strip() for line in text.split("\n") if line.strip()]
    if not chunks:
        chunks = [text]

    results = []
    positive_count = 0
    negative_count = 0
    total_confidence = 0

    for chunk in chunks:
        scores = analyzer.polarity_scores(chunk)
        compound = scores["compound"]

        label = "POSITIVE" if compound >= 0 else "NEGATIVE"
        if label == "POSITIVE":
            positive_count += 1
        else:
            negative_count += 1

        confidence = abs(compound)
        total_confidence += confidence

        results.append({
            "label": label,
            "score": round(confidence, 3),
            "text": chunk,
            "response": generate_response(label)
        })

    total = len(results)
    joy_score = positive_count / total
    anger_score = negative_count / total
    avg_confidence = total_confidence / total

    personality_vector = {
        "joy": round(joy_score, 2),
        "anger": round(anger_score, 2),
        "confidence": round(avg_confidence, 2),
        "chunks_analyzed": total
    }

    return jsonify({
        "personality_vector": personality_vector,
        "raw_results": results
    })


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ReviewPulse backend is running"})