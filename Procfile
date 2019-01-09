release: flask database --delete --force; flask database --init && flask database --populate
web: gunicorn --bind 0.0.0.0:$PORT app:APP
