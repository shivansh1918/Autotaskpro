import os
from app import app

if __name__ == '__main__':
    from waitress import serve

    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    display_host = '127.0.0.1' if host == '0.0.0.0' else host
    print(f"Starting AutoTask Pro at http://{display_host}:{port}")
    serve(app, host=host, port=port)
