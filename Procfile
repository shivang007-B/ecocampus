web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
release: python -c "from app.core.database import create_tables; create_tables()"
worker: celery -A app.tasks worker --loglevel=info
beat: celery -A app.tasks beat --loglevel=info
