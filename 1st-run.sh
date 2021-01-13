#!/bin/sh
#
# this script should be run only the first time the docker image is run,
# in order to populate the mongo db that should be running in a
# different container

# populate the database
python helping_scripts.py

