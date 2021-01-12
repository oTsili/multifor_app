#!/bin/sh
#
# This is just a script that is used to launch the app. It first
# launches a mongo DB instance, populates it with the data (which are
# static anyway) and then starts a gunicorn server. It is meant to be
# used as the CMD to launch when the docker image starts.

# ok, so if a wheel directory is present (mounted as a volume in
# docker), then install the wheels that are in there and replace the
# previously installed ones.  That may be necessary since the
# precompiled tensorflow wheels require AVX instructions and not all
# CPUs have those
if [ -d /wheels ]; then
	pip install -U /wheels/*.whl
fi

# run the DB
mongod --noauth &
sleep 10 # give some time for the db to spin up

# populate the database
python helping_scripts.py

# start the app. Huge timeouts because it takes a long time for a lot of
# actions to be processed
export PYTHONUNBUFFERED=TRUE
gunicorn --bind 0.0.0.0:5000 -t 600 --workers=4 app:app

