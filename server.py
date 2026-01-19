#!/usr/bin/env python
"""
EcoCampus Backend Server
Starts the FastAPI server with Uvicorn
"""
import uvicorn
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting EcoCampus Backend Server...")
    print("📍 Server will run on http://127.0.0.1:8000")
    print("📚 API docs available at http://127.0.0.1:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
