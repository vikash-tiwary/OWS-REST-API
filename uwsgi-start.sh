#!/bin/bash

# Modeled closely after flask portion of amazon/aws-eb-python:3.4.2-onbuild-3.5.1 entrypoint script

cd /var/venv

. bin/activate

cd /var/app

DDTRACE_BINARY=$(whereis ddtrace-run | cut -d ' ' -f 2)
if [ -x ${DDTRACE_BINARY} ]; then
  ${DDTRACE_BINARY} uwsgi --ini uwsgi.ini
else
  uwsgi --ini uwsgi.ini
fi
