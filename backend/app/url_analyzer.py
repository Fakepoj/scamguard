from urllib.parse import urlparse
import re

SHORTENERS = {"bit.ly","tinyurl.com","t.co","goo.gl","is.gd","ow.ly"}
TERMS = ("login","verify","secure","claim","bonus","wallet","update","account")
IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def analyze_url(url):
    parsed = urlparse(url if "://" in url else "http://" + url)
    host = (parsed.hostname or "").lower()
    reasons, suspicious = [], False
    if parsed.username:
        suspicious = True; reasons.append("URL contains embedded userinfo")
    if host in SHORTENERS:
        suspicious = True; reasons.append("URL uses a link-shortening service")
    if IP_RE.match(host):
        suspicious = True; reasons.append("URL uses a raw IP address")
    if host.startswith("xn--") or ".xn--" in host:
        suspicious = True; reasons.append("URL contains punycode")
    if len(host) > 45:
        suspicious = True; reasons.append("Unusually long hostname")
    if any(t in host for t in TERMS):
        suspicious = True; reasons.append("Hostname contains a security-sensitive keyword")
    if parsed.scheme == "http":
        suspicious = True; reasons.append("URL does not use HTTPS")
    return {"url":url,"suspicious":suspicious,"reasons":reasons}
