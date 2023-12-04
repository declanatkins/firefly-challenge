FROM bde2020/spark-submit:3.3.0-hadoop3.3

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/wordcount.py
ENV SPARK_MASTER_NAME "spark"

RUN apk add zlib-dev jpeg-dev gcc musl-dev python3-devi

RUN pip3 install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY source /app
COPY data /data
COPY scripts /scripts

RUN chmod +x /scripts/template.sh
CMD [ "/bin/bash", "/scripts/template.sh" ]
