web: gunicorn --name=mailer --workers=3 --worker-class=gevent --access-logfile=- --error-logfile=- mailer.wsgi:application
