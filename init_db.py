#!/usr/bin/env python
"""Quick database setup script"""

from backend.core.database import create_tables, SessionLocal
from backend.models.user import User
from backend.core.security import get_password_hash
from backend.main import setup_demo_data_sync

try:
    print("Creating database tables...")
    create_tables()
    print("[OK] Database tables created")
    
    db = SessionLocal()
    try:
        setup_demo_data_sync(db)
        print("[OK] Demo campus, emissions, IoT devices and admin user initialized successfully!")
        print("\nDemo Login Credentials:")
        print("  Email: admin@ecocampus.com")
        print("  Password: password123")
    finally:
        db.close()
    
    print("\n[OK] Database setup complete!")
    print("\nTo run backend & frontend:")
    print("  python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000")
    print("  cd frontend && npm run dev")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
