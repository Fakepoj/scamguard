from app.engine import analyze

def test_high_scam():
    r=analyze("URGENT! You won ₦500,000. Send your OTP and pay a clearance fee at https://secure-login.example.com immediately.")
    assert r["risk_level"]=="HIGH"
    assert "credential_request" in r["threats"]

def test_obfuscation():
    r=analyze("URGENT!!! S3ND Y0UR 0TP N0W")
    assert "credential_request" in r["threats"]
    assert r["risk_score"] >= 40

def test_ip_url():
    r=analyze("Verify now at http://192.168.1.55/login")
    assert "suspicious_url" in r["threats"]
    assert r["url_analysis"][0]["suspicious"] is True

def test_safe():
    assert analyze("Hi, are we meeting tomorrow at 10am?")["risk_level"] in {"MINIMAL","LOW"}
