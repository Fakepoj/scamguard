import csv
import math
import re
from collections import Counter
from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "messages.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_FILE = MODEL_DIR / "scam_model.joblib"


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def train():
    texts = []
    labels = []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            texts.append(row["text"])
            labels.append(int(row["label"]))

    scam_docs = [tokenize(text) for text, label in zip(texts, labels) if label == 1]
    safe_docs = [tokenize(text) for text, label in zip(texts, labels) if label == 0]

    scam_counts = Counter(token for doc in scam_docs for token in doc)
    safe_counts = Counter(token for doc in safe_docs for token in doc)

    model = {
        "type": "naive_bayes_text",
        "scam_counts": dict(scam_counts),
        "safe_counts": dict(safe_counts),
        "scam_docs": len(scam_docs),
        "safe_docs": len(safe_docs),
        "vocabulary": list(set(scam_counts) | set(safe_counts)),
    }

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_FILE)

    print(f"Loaded {len(texts)} training samples.")
    print(f"Scam samples: {len(scam_docs)}")
    print(f"Safe samples: {len(safe_docs)}")
    print(f"Model saved to: {MODEL_FILE}")
    print("Training complete.")


if __name__ == "__main__":
    train()