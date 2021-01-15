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

mongoimport --db=multifor \
	--collection=dataframes \
	--file=script_files/dataframes.json
mongoimport --db=multifor \
	--collection=partial_dfs \
	--file=script_files/partial_dfs.json
mongoimport --db=multifor \
	--collection=project_data \
	--file=script_files/project_data.json

