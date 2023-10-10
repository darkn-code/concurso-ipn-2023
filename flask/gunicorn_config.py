gunicorn_app = 'main:app'
bind = '172.20.0.3:8000'
workers = 4
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
