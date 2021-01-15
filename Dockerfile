FROM python:3.6.9
COPY . /app/
WORKDIR /app
RUN apt-get update && \
	apt-get install -y mongo-tools && \
	pip install -r requirements.txt
CMD ["./run.sh"]

