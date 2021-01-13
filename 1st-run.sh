#!/bin/sh
#
# this script should be run only the first time the docker image is run,
# in order to populate the mongo db that should be running in a
# different container

# ok, so if a wheel directory is present (mounted as a volume in
# docker), then install the wheels that are in there and replace the
# previously installed ones.  That may be necessary since the
# precompiled tensorflow wheels require AVX instructions and not all
# CPUs have those
if [ -d /wheels ]; then
	pip install -U /wheels/*.whl
fi

# populate the database
python helping_scripts.py

