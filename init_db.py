#!/usr/bin/env python
"""Quick database setup script"""

from backend.core.database import create_tables, SessionLocal
from backend.models.user import User
from backend.core.security import get_password_hash

try:
    print("Creating database tables...")
    create_tables()
    print("✓ Database tables created")
    
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == 'admin@ecocampus.com').first()
        if not admin:
            print("Creating demo admin user...")
            admin_user = User(
                email='admin@ecocampus.com',
                username='admin',
                full_name='Admin User',
                hashed_password=get_password_hash('password123'),
                role='superuser',
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            print("✓ Admin user created")
            print(f"\nDemo Login:")
            print(f"  Email: admin@ecocampus.com")
            print(f"  Password: password123")
        else:
            print("✓ Admin user already exists")
    finally:
        db.close()
    
    print("\n✓ Database setup complete!")
    print("\nNow run:")
    print("  python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000")
    print("  cd frontend && npm run dev")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
