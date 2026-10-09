import json
from datetime import datetime, timezone
from pathlib import Path

FEEDBACK_FILE = Path("feedback/feedback.jsonl")

def save_feedback(payload):
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    record = {**payload, "timestamp": datetime.now(timezone.utc).isoformat()}
    with FEEDBACK_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record
