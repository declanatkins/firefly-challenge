import argparse
from operator import add
import os
from pyspark.sql import SparkSession
import ops


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--es-host', default='elasticsearch', help='Elasticsearch host', type=str)
    parser.add_argument('--es-port', default=9200, help='Elasticsearch port', type=int)
    parser.add_argument('--allowed-words-file', default='/data/words.txt', help='File containing allowed words', type=str)
    parser.add_argument('--urls-file', default='/data/small-urls', help='File containing urls to process', type=str)
    args = parser.parse_args()

    spark_session = SparkSession.builder.appName("WordCount").getOrCreate()
    lines = spark_session.read.text(args.allowed_words_file).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))

if __name__ == '__main__':
    main()