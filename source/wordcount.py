import argparse
from functools import partial
import json
from operator import add
import string
from pyspark.sql import SparkSession
from newspaper import Article, ArticleException
import requests



def load_article_from_url(url: str) -> str:
    """Loads an article from a url.

        Args:
            url: A string representing a url.

        Returns:
            str: The article text.
    """

    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except ArticleException:
        return ''


def word_tokenize_article(article: str) -> list:
    """Gets words from an article. Also removes punctuation.

        Args:
            article: A string representing an article.

        Returns:
            list: A list of words.
    """

    words = article.split()
    remove_punctuation = str.maketrans('', '', string.punctuation)
    words = [word.translate(remove_punctuation) for word in words]
    words = [word.lower() for word in words]
    return words


def is_valid_word(word: str, es_host: str, es_port: int) -> bool:
    """Determines if a word is valid. len(word) > 2, word contains only letters
        and word is contained in allowed words.

        Args:
            word: A string representing a word.
            es_host: A string representing the Elasticsearch host.
            es_port: An int representing the Elasticsearch port.
        
        Returns:
            bool: True if word is valid, False otherwise.
    """

    if len(word) <= 2 or not word.isalpha():
        return False

    result = requests.get(f'http://{es_host}:{es_port}/allowed-words/_search?q=word:{word}')

    if result.status_code != 200:
        raise ValueError(f'Error querying Elasticsearch: {result.json()}')
    return result.json()['hits']['total']['value'] >= 1

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--es-host', default='elasticsearch', help='Elasticsearch host', type=str)
    parser.add_argument('--es-port', default=9200, help='Elasticsearch port', type=int)
    parser.add_argument('--allowed-words-file', default='/data/words.txt', help='File containing allowed words', type=str)
    parser.add_argument('--urls-file', default='/data/endg-urls', help='File containing urls to process', type=str)
    args = parser.parse_args()

    spark_session = SparkSession.builder.appName("WordCount").getOrCreate()
    is_valid_word_partial = partial(is_valid_word, es_host=args.es_host, es_port=args.es_port)

    urls = spark_session.read.text(args.urls_file).rdd.map(lambda r: r[0])
    articles = urls.map(load_article_from_url)
    words = articles.flatMap(word_tokenize_article)
    valid_words = words.filter(is_valid_word_partial)
    word_counts = valid_words.map(lambda word: (word, 1)).reduceByKey(add)

    # Get the top 10 words
    top_words = word_counts.map(lambda x: (x[1], x[0])).sortByKey(False).take(10)
    top_words_dict = {word: count for count, word in top_words}

    print('*** Top 10 words ***')
    print(json.dumps(top_words_dict, indent=4))

if __name__ == '__main__':
    main()