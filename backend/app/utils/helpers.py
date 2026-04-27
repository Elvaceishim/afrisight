import re


def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_market(text: str) -> str:
    lower = text.lower()
    if any(kw in lower for kw in ["nigeria", "lagos", "abuja"]):
        return "ng"
    if any(kw in lower for kw in ["kenya", "nairobi", "m-pesa", "mpesa"]):
        return "ke"
    if any(kw in lower for kw in ["tanzania", "dar es salaam", "dar"]):
        return "tz"
    if any(kw in lower for kw in ["congo", "kinshasa", "drc", "democratic republic"]):
        return "cd"
    if any(kw in lower for kw in ["ethiopia", "addis", "addis ababa"]):
        return "et"
    if any(kw in lower for kw in ["africa", "pan-african", "pan african"]):
        return "pan-african"
    return "unknown"


def format_duration(seconds: float) -> str:
    minutes = int(seconds // 60)
    remaining = int(seconds % 60)
    if minutes > 0:
        return f"{minutes}m {remaining}s"
    return f"{remaining}s"
