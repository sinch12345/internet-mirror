from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()
print("VADER sentiment analyzer ready.")


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

        results.append({"label": label, "score": round(confidence, 3), "text": chunk})

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
    return jsonify({"status": "Internet Mirror backend is running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)