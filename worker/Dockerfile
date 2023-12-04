FROM bde2020/spark-worker:3.3.0-hadoop3.3

RUN apk add zlib-dev jpeg-dev gcc musl-dev python3-dev

RUN pip3 install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt