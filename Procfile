web: gunicorn Tudulu.wsgi
worker: celery -A Tudulu worker --loglevel=info
beat: celery -A Tudulu beat --loglevel=info
