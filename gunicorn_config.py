# Gunicorn Configuration pour production
# brainblue_config.py

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = os.getenv("ACCESS_LOG", "-")
errorlog = os.getenv("ERROR_LOG", "-")
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "brainblue-api"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (configure with Nginx reverse proxy)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Server hooks
def on_starting(server):
    print("Gunicorn server starting BRAINBLUE URBAIN...")

def when_ready(server):
    print("Gunicorn server ready. Spawning workers...")

def on_exit(server):
    print("Gunicorn server stopping...")

# Maximum number of pending connections
max_requests = 1000
max_requests_jitter = 50

# Graceful timeout
graceful_timeout = 30

# Preload application code before forking worker processes
preload_app = True

# Automatic reloader for development changes
reload = os.getenv("FLASK_ENV", "production") == "development"
reload_extra_files = []

# Monitoring
statsD = False
# statsD_host = "localhost:8125"
# statsD_prefix = "brainblue"
