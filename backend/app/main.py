from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import AnalyzeRequest, AnalyzeResponse, FeedbackRequest
from app.engine import analyze
from app.ocr import extract_text
from app.feedback import save_feedback

app = FastAPI(title="ScamGuard", version="0.5.1", description="Multimodal scam detection API with hybrid ML, local scam intelligence, OCR and feedback collection.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health(): return {"status":"ok","version":"0.5.1"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_message(request: AnalyzeRequest): return analyze(request.text)

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    allowed = {"image/png","image/jpeg","image/webp"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=415, detail="Upload a PNG, JPEG or WebP image.")
    data = await file.read()
    if len(data) > 8 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image must be 8 MB or smaller.")
    try:
        text = extract_text(data)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"OCR processing failed: {exc}")
    if not text:
        raise HTTPException(status_code=422, detail="No readable text was detected in the image.")
    result = analyze(text)
    result["extracted_text"] = text
    result["source"] = "image_ocr"
    return result

@app.post("/feedback")
def feedback(request: FeedbackRequest):
    return {"status":"saved", "feedback": save_feedback(request.model_dump())}
