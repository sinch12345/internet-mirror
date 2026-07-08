# 🔮 The Internet Mirror

A living, breathing 3D sculpture that visualizes the emotional tone of your written text — built with Three.js on the frontend and a DistilBERT sentiment model on the backend.

## What it does

Paste in a block of text (comments, posts, journal entries — one per line), and the app:
1. Runs each line through a sentiment analysis model
2. Builds a "personality vector" (joy score, anger score, confidence)
3. Morphs a 3D avatar in real time — its **color** shifts from calm green to angry red, its **surface** goes from smooth to spiky, and its **spin speed** increases with joy

## Demo

*(Add a screenshot or GIF here once deployed — this matters a lot for recruiters skimming your repo)*

## Tech Stack

- **Frontend:** HTML/CSS/JavaScript + Three.js (WebGL 3D rendering)
- **Backend:** Flask (Python)
- **AI:** HuggingFace Transformers — `distilbert-base-uncased-finetuned-sst-2-english`

## Running locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
python app.py
```
Server runs at `http://127.0.0.1:5000`

### Frontend
Open `frontend/index.html` with VS Code's Live Server extension (or any static file server).

## Why I built this

To explore the intersection of machine learning and interactive visual design — turning abstract sentiment scores into something you can actually *see* change in real time, rather than a table of numbers.

## Roadmap

- [ ] Deploy live demo
- [ ] Add more personality dimensions (sadness, technical jargon)
- [ ] "Toxicity Cleaner" — AI-rewritten polite version of negative text