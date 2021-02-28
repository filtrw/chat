FROM python:3


WORKDIR /usr/src/app

RUN pip install --no-cache-dir psycopg2-binary


COPY . .
ENV BD_HOST "host.docker.internal"
CMD [ "python", "./server.py" ]
