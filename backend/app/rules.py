import re

URL_RE = re.compile(r"https?://[^\s<>()]+|www\.[^\s<>()]+", re.I)

RULES = [
("urgency",12,r"\b(urgent|immediately|act now|hurry|limited time|expire|today only|now now)\b"),
("financial_bait",18,r"(won|winner|prize|giveaway|bonus|free money|million|jackpot|cash reward|₦[\d,]+|\$[\d,]+)"),
("credential_request",22,r"\b(password|otp|pin|cvv|verification code|login details|account details)\b"),
("impersonation",16,r"\b(bank|support team|customer care|official|security team|admin|manager|police|customs)\b"),
("payment_request",18,r"\b(pay|payment|transfer|send money|fee|clearance fee|processing fee|activation fee)\b"),
("secrecy",10,r"\b(keep this secret|don't tell anyone|do not tell anyone|confidential)\b"),
("remote_access",18,r"\b(anydesk|teamviewer|remote access|screen share|install this app)\b"),
("job_scam",14,r"\b(work from home|job opportunity|vacancy|registration fee|employment fee)\b"),
("romance_manipulation",10,r"\b(love|darling|baby|emergency|hospital bill|travel money)\b"),
]

def extract_urls(text):
    return [u.rstrip(".,!?;:)]}") for u in URL_RE.findall(text)]

def run_rules(text):
    score, threats, indicators = 0, [], []
    for name, weight, pattern in RULES:
        if re.search(pattern, text, re.I):
            score += weight
            threats.append(name)
            indicators.append("Detected " + name.replace("_", " "))
    return min(score,100), threats, indicators
