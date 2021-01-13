#!/bin/sh
#
# This is just a script that is used to launch the app. It installs any
# wheels that may be around and then starts a gunicorn server. It is
# meant to be used as the CMD to launch when the docker image starts.
# NOTE: the first time the container is run, you should run the
# 1st-run.sh script instead.

# ok, so if a wheel directory is present (mounted as a volume in
# docker), then install the wheels that are in there and replace the
# previously installed ones.  That may be necessary since the
# precompiled tensorflow wheels require AVX instructions and not all
# CPUs have those
if [ -d /wheels ]; then
	pip install -U /wheels/*.whl
fi

# start the app. Huge timeouts because it takes a long time for a lot of
# actions to be processed
export PYTHONUNBUFFERED=TRUE
gunicorn --bind 0.0.0.0:5000 -t 600 --workers=4 app:app

