from app.normalize import normalize_text
from app.rules import extract_urls, run_rules
from app.url_analyzer import analyze_url
from app.ml import predict
from app.local_intel import analyze_local


def _dedupe_urls(urls):
    seen = set()
    result = []
    for url in urls:
        key = url.strip().rstrip(".,!?;:)]}").lower()
        if key not in seen:
            seen.add(key)
            result.append(url.strip().rstrip(".,!?;:)]}"))
    return result


def _confidence(rule_score, ml_probability, url_bonus, ml_available):
    rule_strength = rule_score / 100.0
    url_strength = min(url_bonus, 30) / 30.0

    if not ml_available:
        # Confidence reflects evidence strength without pretending an ML model ran.
        return round(min(0.95, 0.55 + 0.30 * rule_strength + 0.10 * url_strength), 3)

    agreement = 1.0 - abs(rule_strength - ml_probability)
    evidence = 0.55 * agreement + 0.30 * rule_strength + 0.15 * url_strength
    return round(min(0.99, max(0.50, evidence)), 3)


def analyze(text):
    normalized = normalize_text(text)
    rule_score, threats, indicators = run_rules(normalized)
    local_categories, local_indicators = analyze_local(normalized)

    if local_categories:
        rule_score = min(100, rule_score + min(20, 5 * len(local_categories)))
        threats.extend([f"local_{x}" for x in local_categories])
        indicators.extend(local_indicators)

    urls = _dedupe_urls(extract_urls(text))
    url_analysis, url_bonus = [], 0
    for url in urls:
        result = analyze_url(url)
        url_analysis.append(result)
        if result["suspicious"]:
            url_bonus += min(15, 5 * len(result["reasons"]))
            threats.append("suspicious_url")
            indicators.extend(result["reasons"])

    ml_probability, ml_available = predict(normalized)
    
    ml_score = round(ml_probability * 100) if ml_available else 0

    hybrid_score = round(
        0.55 * rule_score + 0.35 * ml_score + 0.10 * min(url_bonus, 30)
    )
    # A hybrid model must not downgrade strong deterministic evidence.
    score = max(rule_score, hybrid_score)

    if rule_score >= 55:
        score = max(score, 60)
    if "credential_request" in threats:
        score = max(score, 40)
    if "credential_request" in threats and "payment_request" in threats:
        score = max(score, 75)
    if local_categories and any(
        x in local_categories for x in ("bank_impersonation", "whatsapp_takeover", "agency_impersonation")
    ):
        score = max(score, 55)

    score = min(100, score)
    level = "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW" if score >= 15 else "MINIMAL"
    confidence = _confidence(rule_score, ml_probability or 0.0, url_bonus, ml_available)

    recommendation = {
        "HIGH": "Do not click links, send money, install remote-access software, or share passwords, OTPs, PINs, or personal information. Verify independently through an official channel.",
        "MEDIUM": "Pause and independently verify the sender, organization, payment request, and any link before taking action.",
        "LOW": "Some suspicious indicators were found. Avoid sharing sensitive information until the request is verified.",
        "MINIMAL": "No strong scam indicators were detected. This does not guarantee that the message is safe.",
    }[level]

    return {
        "risk_score": score,
        "risk_level": level,
        "confidence": confidence,
        "threats": sorted(set(threats)),
        "indicators": sorted(set(indicators)),
        "recommendation": recommendation,
        "urls": urls,
        "url_analysis": url_analysis,
        "rule_score": rule_score,
        "ml_probability": round(ml_probability, 4) if ml_available else 0.0,
        "ml_available": ml_available,
        "normalized_text": normalized,
        "scam_categories": local_categories,
        "local_indicators": local_indicators,
    }
