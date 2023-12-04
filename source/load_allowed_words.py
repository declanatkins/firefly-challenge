"""Spark task to load allowed words into Elasticsearch
"""

import argparse
import elasticsearch
from elasticsearch import helpers
from pyspark.sql import SparkSession


def is_valid_word(word: str) -> bool:
    """Determines if a word is valid. len(word) > 2 and word contains only letters.

        Args:
            word: A string representing a word.
        
        Returns:
            bool: True if word is valid, False otherwise.
    """

    return len(word) > 2 and word.isalpha()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--es-host', default='elasticsearch', help='Elasticsearch host', type=str)
    parser.add_argument('--es-port', default=9200, help='Elasticsearch port', type=int)
    parser.add_argument('--allowed-words-file', default='/data/words.txt', help='File containing allowed words', type=str)
    args = parser.parse_args()

    spark_session = SparkSession.builder.appName("LoadAllowedWords").getOrCreate()
    lines = spark_session.read.text(args.allowed_words_file).rdd.map(lambda r: r[0])
    words = lines.filter(is_valid_word)

    client = elasticsearch.Elasticsearch([{'host': args.es_host, 'port': args.es_port, 'scheme': 'http'}])
    client.options(ignore_status=[404]).indices.delete(index='allowed-words')
    client.indices.create(index='allowed-words')

    batch = []
    for i, word in enumerate(words.collect()):
        batch.append({
            '_index': 'allowed-words',
            '_id': i,
            'word': word
        })
        if len(batch) >= 5000:
            helpers.bulk(client, batch)
            batch = []
    else:
        if batch:
            helpers.bulk(client, batch)


if __name__ == '__main__':
    main()