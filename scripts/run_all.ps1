Write-Host "Building Spark worker..."
docker-compose build

Write-Host "Creating Cluster..."
docker-compose up -d --scale spark-worker=3

Write-Host "Building load words task..."
docker build -t load_words --build-arg SCRIPT_PATH=load_words.py .

Write-Host "Building word count task..."
docker build -t wordcount .

Write-Host "Running load words task..."
docker run --name load_words -e ENABLE_INIT_DAEMON=false --link spark:spark --net firefly-challenge_spark-network --rm -it load_words

Write-Host "Running word count task..."
docker run --name wordcount -e ENABLE_INIT_DAEMON=false --link spark:spark --net firefly-challenge_spark-network --rm -it wordcount