release: flask database --delete --force
release: flask database --init
web: gunicorn --bind 0.0.0.0:$PORT app:APP