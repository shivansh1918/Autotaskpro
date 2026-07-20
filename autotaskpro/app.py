from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import time
from werkzeug.utils import secure_filename
from automation.move_files import move_images
from automation.extract_emails import extract_emails_from_file
from automation.scrape_data import scrape_page

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
EXTRACTED_DIR = os.path.join(BASE_DIR, 'extracted')

for d in (UPLOAD_DIR, OUTPUT_DIR, EXTRACTED_DIR):
    os.makedirs(d, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'dev-secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # List available generated files for download
    output_files = os.listdir(OUTPUT_DIR) if os.path.exists(OUTPUT_DIR) else []
    extracted_files = os.listdir(EXTRACTED_DIR) if os.path.exists(EXTRACTED_DIR) else []
    return render_template('dashboard.html', output_files=output_files, extracted_files=extracted_files)

@app.route('/move', methods=['POST'])
def move():
    files = request.files.getlist('move_files')
    if not files or all(f.filename == '' for f in files):
        flash('No files uploaded for moving', 'error')
        return redirect(url_for('dashboard'))

    timestamp = int(time.time())
    session_dir = os.path.join(UPLOAD_DIR, f'move_{timestamp}')
    os.makedirs(session_dir, exist_ok=True)

    for f in files:
        if f and f.filename:
            filename = secure_filename(f.filename)
            f.save(os.path.join(session_dir, filename))

    moved_count, moved_files = move_images(session_dir, os.path.join(OUTPUT_DIR, 'moved_files'))

    report_path = os.path.join(OUTPUT_DIR, 'moved_files_report.txt')
    with open(report_path, 'w', encoding='utf-8') as r:
        r.write(f'Moved files: {moved_count}\n')
        for p in moved_files:
            r.write(p + '\n')

    flash(f'Moved {moved_count} JPG files', 'success')
    return redirect(url_for('dashboard'))

@app.route('/extract', methods=['POST'])
def extract():
    f = request.files.get('text_file')
    if not f or f.filename == '':
        flash('No text file uploaded', 'error')
        return redirect(url_for('dashboard'))
    filename = secure_filename(f.filename)
    saved = os.path.join(UPLOAD_DIR, filename)
    f.save(saved)

    emails = extract_emails_from_file(saved)
    out_path = os.path.join(EXTRACTED_DIR, 'extracted_emails.txt')
    with open(out_path, 'w', encoding='utf-8') as out:
        for e in sorted(emails):
            out.write(e + '\n')

    flash(f'Extracted {len(emails)} unique emails', 'success')
    return redirect(url_for('dashboard'))

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('page_url', '').strip()
    if not url:
        flash('No URL provided', 'error')
        return redirect(url_for('dashboard'))

    title, text = scrape_page(url)
    out_path = os.path.join(OUTPUT_DIR, 'scraped_content.txt')
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(f'Title: {title}\n\n')
        out.write(text)

    flash('Page scraped successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/downloads/<path:filename>')
def downloads(filename):
    # Serve files from output or extracted folders
    for folder in (OUTPUT_DIR, EXTRACTED_DIR):
        fp = os.path.join(folder, filename)
        if os.path.exists(fp):
            return send_from_directory(folder, filename, as_attachment=True)
    flash('File not found', 'error')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    from waitress import serve

    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    display_host = '127.0.0.1' if host == '0.0.0.0' else host
    print(f"Starting AutoTask Pro at http://{display_host}:{port}")
    serve(app, host=host, port=port)
