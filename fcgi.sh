#!/bin/bash

# Replace these three settings.
PROJDIR="/home/django/cpu/"
PIDFILE="$PROJDIR/cpu.pid"
SOCKET="$PROJDIR/cpu.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi


exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi method="threaded" host=127.0.0.1 port=3033 pidfile=$PIDFILE
