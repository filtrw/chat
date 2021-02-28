FROM python:3

ENV BD_HOST "host.docker.internal"
WORKDIR /usr/src/app
RUN pip install --no-cache-dir psycopg2-binary
COPY . .

CMD [ "python", "./server.py" ]
