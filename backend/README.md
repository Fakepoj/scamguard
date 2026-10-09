# SCAMGUARD v0.5

SCAMGUARD v0.5 extends the hybrid scam detector into a multimodal security product.

## New in v0.5
- Screenshot/image analysis with OCR
- PNG, JPEG and WebP uploads
- Image preprocessing before OCR
- Nigerian/local scam intelligence patterns
- Bank/customer-care impersonation patterns
- POS/payment-agent patterns
- Naira payment detection
- Fake recruitment fee patterns
- Investment/guaranteed-return patterns
- WhatsApp/account-takeover patterns
- Government/agency impersonation patterns
- Social-engineering patterns
- User feedback endpoint for future model improvement
- CORS support for the React frontend
- Expanded automated tests

## Architecture

Text or Screenshot -> OCR/Normalization -> Rules -> Local Intelligence -> URL Intelligence -> ML -> Hybrid Risk Engine -> Report -> Feedback

## Setup

```powershell
python -m pip install -r requirements.txt
python train.py
python -m pytest -q
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## OCR requirement

The Python `pytesseract` package is only a wrapper. You must also install the **Tesseract OCR engine** on Windows and make sure `tesseract.exe` is available on PATH. If it is not on PATH, set `pytesseract.pytesseract.tesseract_cmd` in `app/ocr.py` to your installed executable path.

## API

### POST `/analyze`
Analyze plain text.

### POST `/analyze-image`
Upload a PNG/JPEG/WebP screenshot. OCR extracts the text and sends it through the same SCAMGUARD engine.

### POST `/feedback`
Stores `scam` or `safe` labels in `feedback/feedback.jsonl` for later dataset/model improvement.

## Important

The local rules are heuristics, not proof that a sender or organization is fraudulent. The ML model uses the small synthetic development dataset inherited from v0.3. Before production use, evaluate against a large, representative, consented dataset and measure false positives, false negatives and performance across languages and channels.
