release: flask database --delete --force
release: flask database --init
release: flask database --populate
web: gunicorn --bind 0.0.0.0:$PORT app:APP