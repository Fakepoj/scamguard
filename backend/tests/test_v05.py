from app.local_intel import analyze_local
from app.engine import analyze

def test_local_bank_pattern():
    cats, indicators = analyze_local("GTBank support says send your OTP to verify your account")
    assert "bank_impersonation" in cats
    assert indicators

def test_naira_detection():
    cats, _ = analyze_local("Send ₦50,000 now for account activation")
    assert "naira_payment" in cats

def test_engine_has_v05_fields():
    result = analyze("Urgent! Send your OTP and PIN to verify your GTBank account.")
    assert "scam_categories" in result
    assert "local_indicators" in result
    assert result["risk_score"] >= 40


def test_duplicate_urls_are_removed():
    result = analyze("Join https://chat.whatsapp.com/ABC now: https://chat.whatsapp.com/ABC")
    assert result["urls"] == ["https://chat.whatsapp.com/ABC"]
    assert len(result["url_analysis"]) == 1


def test_strong_rule_score_is_not_downgraded():
    result = analyze("URGENT! Your bank account will be suspended. Send OTP and PIN immediately.")
    assert result["risk_score"] >= result["rule_score"]


def test_ml_availability_is_explicit():
    result = analyze("Please send your OTP immediately.")
    assert "ml_available" in result
