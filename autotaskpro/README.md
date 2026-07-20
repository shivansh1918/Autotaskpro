# AutoTask Pro

AutoTask Pro is a lightweight Flask web application that automates common file and email tasks: moving JPEGs, extracting emails from text, and scraping page content.

## Features
- Move JPG files uploaded by the user and generate a report
- Extract emails from uploaded .txt files (deduplicated)
- Scrape a webpage (title + text) and save results
- Modern responsive UI with glassmorphism and dark mode

## Install

1. Create a virtualenv and activate it

```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS / Linux
pip install -r requirements.txt
```

2. Run the app

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Folder structure

AutoTaskPro/
 - app.py
 - requirements.txt
 - README.md
 - templates/
    - index.html
    - dashboard.html
 - static/
    - style.css
    - app.js
    - images/logo.svg
 - uploads/ (user uploads)
 - output/ (generated reports)
 - extracted/ (extracted data)
 - automation/
    - move_files.py
    - extract_emails.py
    - scrape_data.py

## How to use

- Visit the Dashboard. Use the cards to upload files or provide a URL.
- After running an action, download generated files from the links.

## Notes
- The scraper is intentionally simple and uses regex to strip HTML. For heavy scraping use BeautifulSoup.
- Error handling and edge-cases are handled with simple flashes.
