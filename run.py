import os
import sys
import subprocess

# If running outside the project virtual environment, auto-switch to .venv
base_dir = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(base_dir, ".venv", "Scripts", "python.exe")

if os.path.exists(venv_python):
    curr_exe = os.path.abspath(sys.executable).lower()
    target_exe = os.path.abspath(venv_python).lower()
    if curr_exe != target_exe:
        print("[*] Switching to project virtual environment (.venv)...")
        sys.exit(subprocess.call([venv_python] + sys.argv))

import time
import threading
import webbrowser
import uvicorn

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("   PocketSmart AI: Smart Budget & Recommendation Assistant")
    print("=" * 65)
    print("\n[+] Starting FastAPI server...")
    print("[+] Website URL : http://127.0.0.1:8000")
    print("[+] API Docs    : http://127.0.0.1:8000/docs")
    print("\nOpening http://127.0.0.1:8000 in your browser...")
    print("Press Ctrl+C to stop the server.\n")
    
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
