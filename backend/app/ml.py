import math
import re
from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "scam_model.joblib"


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def predict(text):
    if not MODEL_PATH.exists():
        return 0.0, False

    model = joblib.load(MODEL_PATH)

    tokens = tokenize(text)

    scam_counts = model.get("scam_counts", {})
    safe_counts = model.get("safe_counts", {})

    scam_docs = model.get("scam_docs", 1)
    safe_docs = model.get("safe_docs", 1)

    vocabulary = model.get("vocabulary", [])
    vocabulary_size = max(len(vocabulary), 1)

    scam_total = sum(scam_counts.values())
    safe_total = sum(safe_counts.values())

    if not scam_total or not safe_total:
        return 0.0, False

    scam_log_prob = math.log(scam_docs / (scam_docs + safe_docs))
    safe_log_prob = math.log(safe_docs / (scam_docs + safe_docs))

    for token in tokens:
        scam_probability = (
            scam_counts.get(token, 0) + 1
        ) / (scam_total + vocabulary_size)

        safe_probability = (
            safe_counts.get(token, 0) + 1
        ) / (safe_total + vocabulary_size)

        scam_log_prob += math.log(scam_probability)
        safe_log_prob += math.log(safe_probability)

    difference = scam_log_prob - safe_log_prob

    probability = 1 / (1 + math.exp(-max(min(difference, 20), -20)))

    return round(probability, 4), True