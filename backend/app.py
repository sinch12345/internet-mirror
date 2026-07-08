from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # allows frontend (running on a different port) to talk to this server

print("Loading sentiment model... (this happens once, may take a minute)")
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
print("Model loaded. Server ready.")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    # Split into rough "chunks" (like separate comments), one per line
    chunks = [line.strip() for line in text.split("\n") if line.strip()]
    if not chunks:
        chunks = [text]

    results = sentiment_analyzer(chunks)

    # Build the "personality vector"
    positive_count = 0
    negative_count = 0
    total_confidence = 0

    for r in results:
        total_confidence += r["score"]
        if r["label"] == "POSITIVE":
            positive_count += 1
        else:
            negative_count += 1

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