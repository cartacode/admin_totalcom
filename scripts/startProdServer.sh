#!/bin/sh
echo "
Production Server
Commands to consider:

$ cd /home/ubuntu/admin_totalcom   
$ ./manage collectstatic   <-- put all static files into /static

# gunicorn is running
$ sudo systemctl status gunicorn  <-- serves django project to nginx from <project>/gf/wsgi.py
$ sudo journalctl -u gunicorn.service  <-- shows errors



