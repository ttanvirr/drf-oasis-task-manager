import os

bind = "0.0.0.0:8000"
workers = int(os.getenv("GUNICORN_WORKERS", "2"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))
graceful_timeout = 30
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = "info"
max_requests = 1000
max_requests_jitter = 100
