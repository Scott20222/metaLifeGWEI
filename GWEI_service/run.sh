gunicorn -w 2 -b 0.0.0.0:5050 server:app > server.log & python3 executor.py > run.log
