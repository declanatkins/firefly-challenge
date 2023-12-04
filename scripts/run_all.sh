#!/bin/bash

echo "Building Spark worker..."
docker-compose build

echo "Creating Cluster..."
docker-compose up -d --scale spark-worker=3

echo "Building load words task..."
docker build -t load_words --build-arg SCRIPT_PATH=load_allowed_words.py .

echo "Building word count task..."
docker build -t word_count .

echo "Running load words task..."
docker run --name load_words -e ENABLE_INIT_DAEMON=false --link spark:spark --net firefly-challenge_spark-network --rm -it load_words

echo "Running word count task..."
docker run --name wordcount -e ENABLE_INIT_DAEMON=false --link spark:spark --net firefly-challenge_spark-network --rm -it wordcount