import re

LOCAL_RULES = [
    ("bank_impersonation", "Possible Nigerian bank/customer-care impersonation", r"\b(access bank|gtbank|gt bank|first bank|uba|zenith bank|opay|palmpay|moniepoint|kuda|sterling bank|union bank|fcmb)\b.*\b(otp|pin|cvv|password|verify|account)\b"),
    ("pos_agent_scam", "Possible POS/payment-agent scam", r"\b(pos|agent|terminal)\b.*\b(activation|clearance|unlock|fee|charge|transfer)\b"),
    ("naira_payment", "Naira-denominated payment request detected", r"(?:₦|\bngn\b|\bnaira\b)\s*[\d,]+|[\d,]+\s*(?:₦|ngn|naira)\b"),
    ("fake_job_fee", "Possible recruitment scam involving a fee", r"\b(job|employment|recruitment|vacancy)\b.*\b(registration|processing|training|activation|employment)\s*fee\b"),
    ("investment_pitch", "Possible high-pressure investment/returns pitch", r"\b(crypto|forex|investment|invest)\b.*\b(guaranteed|profit|returns|double|triple|daily)\b"),
    ("whatsapp_takeover", "Possible WhatsApp/account-takeover pattern", r"\b(whatsapp|account)\b.*\b(otp|verification code|six digit|6 digit)\b"),
    ("agency_impersonation", "Possible government/agency impersonation", r"\b(nysc|jamb|frsc|customs|immigration|police|efcc|inec|federal government)\b.*\b(payment|fee|verify|registration|claim)\b"),
    ("social_engineering", "Social-engineering language detected", r"\b(mummy|mama|daddy|dad|mum|brother|sister)\b.*\b(send|transfer|urgent|money)\b"),
]

def analyze_local(text):
    indicators=[]; categories=[]
    for name, indicator, pattern in LOCAL_RULES:
        if re.search(pattern, text, re.I):
            categories.append(name)
            indicators.append(indicator)
    return sorted(set(categories)), indicators
