import re

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

def extract_emails_from_text(text):
    found = EMAIL_RE.findall(text)
    return set(found)

def extract_emails_from_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return extract_emails_from_text(text)
