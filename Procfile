web: gunicorn app:app --timeout 120
worker: celery -A app.celery worker --loglevel=info
