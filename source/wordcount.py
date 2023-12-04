import argparse
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
    