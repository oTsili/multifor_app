FROM python:3.7
COPY . /app/
WORKDIR /app
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | \
		apt-key add - && \
	echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.2 main" | \
		tee /etc/apt/sources.list.d/mongodb-org-4.2.list && \
	apt-get update && \
	apt-get install -y mongodb-org && \
	mkdir -p /data/db && \
	pip install -r requirements.txt
CMD ["./run.sh"]

