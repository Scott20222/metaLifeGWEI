gunicorn -w 4 -b 0.0.0.0:5050 server:app  > server.log & python executor.py > run.log
