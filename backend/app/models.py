from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)

class URLAnalysis(BaseModel):
    url: str
    suspicious: bool
    reasons: list[str]

class AnalyzeResponse(BaseModel):
    risk_score: int
    risk_level: str
    confidence: float
    threats: list[str]
    indicators: list[str]
    recommendation: str
    urls: list[str]
    url_analysis: list[URLAnalysis]
    rule_score: int
    ml_probability: float
    ml_available: bool = False
    normalized_text: str
    scam_categories: list[str] = []
    local_indicators: list[str] = []

class FeedbackRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)
    label: str = Field(pattern="^(scam|safe)$")
    risk_score: int = Field(ge=0, le=100)
    risk_level: str
