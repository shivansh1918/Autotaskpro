import re

# optional requests import; if missing, scraper will fail gracefully
try:
    import requests
    _HAVE_REQUESTS = True
except Exception:
    requests = None
    _HAVE_REQUESTS = False

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
STRIP_TAGS = re.compile(r'<[^>]+>')

def scrape_page(url, timeout=8):
    if not _HAVE_REQUESTS:
        return '', ''
    try:
        resp = requests.get(url, timeout=timeout, headers={'User-Agent': 'AutoTaskPro/1.0'})
        resp.raise_for_status()
        html = resp.text
        title_match = TITLE_RE.search(html)
        title = title_match.group(1).strip() if title_match else ''
        # naive body extraction
        text = STRIP_TAGS.sub(' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        return title, text[:20000]
    except Exception:
        return '', ''
