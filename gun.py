import os
bind = '0.0.0.0:8000'
workers = 4
backlog = 2048
worker_class = "gevent"
debug = True
proc_name = 'gunicorn.proc'