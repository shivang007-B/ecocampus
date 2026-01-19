#!/usr/bin/env python
"""
Simple script to run the backend server
"""
import subprocess
import sys
import time

while True:
    try:
        print("Starting backend server...")
        proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd="."
        )
        proc.wait()
        print("Backend stopped, restarting in 5 seconds...")
        time.sleep(5)
    except KeyboardInterrupt:
        print("Shutting down...")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
