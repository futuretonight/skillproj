"""
SkillBridge AI - One-Click Local Launcher
Run this file to automatically start the backend server and open the web dashboard in your browser.

Usage:
    python run.py
"""

import sys
import os
import time
import threading
import webbrowser

# Ensure directories are in sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def open_browser():
    """Wait for server startup and open browser."""
    time.sleep(1.5)
    url = "http://localhost:8000"
    print(f"\n🌐 Opening web application in your browser: {url}")
    webbrowser.open(url)


def main():
    print("=" * 65)
    print("  🚀 SkillBridge AI — Employment & Skilling Impact Platform")
    print("=" * 65)
    print("  • Web Application : http://localhost:8000")
    print("  • Interactive API : http://localhost:8000/docs")
    print("  • Press CTRL + C to stop the server at any time")
    print("=" * 65 + "\n")

    try:
        import uvicorn
    except ImportError:
        print("Installing required dependencies...")
        os.system(f'"{sys.executable}" -m pip install -r requirements.txt')
        import uvicorn

    from backend.main import app

    # Launch browser in a background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start the server
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
