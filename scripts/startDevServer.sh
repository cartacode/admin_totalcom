#!/bin/sh
if [ "$VIRTUAL_ENV" != "$" ]
then
    printf "NOT running inside 'admin_totalcom' virtualenv\nRun: 'source ../venv/bin/activate'\n\n"
    exit
fi
echo "Browse to: localhost:8000 or <ip address>:8000 on other systems\n"
cd $ADMIN_TOTALCOM_ROOT
./manage.py runserver 0:8000
