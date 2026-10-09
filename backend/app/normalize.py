import re
import unicodedata

LEET_MAP = str.maketrans({"@":"a","0":"o","1":"i","3":"e","4":"a","5":"s","7":"t","$":"s"})

def normalize_text(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).translate(LEET_MAP)
    value = re.sub(r"(.)\1{3,}", r"\1\1", value)
    value = re.sub(r"[_\-*]+", " ", value)
    return re.sub(r"\s+", " ", value).strip().lower()
