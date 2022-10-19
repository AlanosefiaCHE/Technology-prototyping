import deep_translator
import nltk
import pygal
import tweepy

from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer

CLIENT = tweepy.Client(
    'AAAAAAAAAAAAAAAAAAAAAG9EhAEAAAAA%2BLR%2BJ1%2FpM0UC5y9QfHxPND7ccAI%3DvHGlimS0Gz93SWTqFglsr2J3PkYGUfLd7S7czHwsXyRMww8dNZ',
    return_type=dict)

SID = SentimentIntensityAnalyzer()

class Error(Exception):
    pass

def get_twitter_id(username):
    """Get_twitter_id takes a username and returns the corresponding twitter id."""
    response = CLIENT.get_users(usernames=[username])

    # Instead of `response['data']` do `if 0 in response['data']`
    if 'data' in response and response['data'] and 'id' in response['data'][0]:
        return response['data'][0]['id']
    else:
        raise Error

def get_tweets(id, from_date, max_results=32, until_date=datetime.now()):
    """Get_tweets takes an id, max_results, from_date and an until_date and returns tweets as a list of strings."""
    tweets_list = []

    tweets = CLIENT.get_users_tweets(
        id=id,
        end_time=until_date,
        max_results=max_results,
        start_time=from_date)

    for tweet in tweets['data']:
        tweets_list.append(tweet['text'])

    return tweets_list


def translate_tweets(tweets):
    """Translate_tweets takes a list of strings and returns a list of strings translated to english."""
    return deep_translator.GoogleTranslator(source="auto", target="en").translate_batch(tweets)


def analyze_tweets(tweets):
    """Analyze_tweets takes a list of strings and returns a list of the vader compound scores per entry in this list."""
    scores = []

    for tweet in tweets:
        sentences = nltk.sent_tokenize(tweet)

        result_sum = 0
        sentences_amount = len(sentences)

        for sentence in sentences:
            ss = SID.polarity_scores(sentence)
            result_sum += ss['compound']

        scores.append(result_sum / sentences_amount)

    return scores


def plot_tweets(tweet_scores):
    """Plot_tweets takes in a list of numbers and returns a pygal plot encoded in data_uri."""
    line_chart = pygal.Line(
        show_legend=False,
        x_title='Tweet number (new to old)',
        y_title='Compound score')
    line_chart.y_labels = [-1, -0.05, 0, 0.05, 1]
    line_chart.x_labels = [*range(1, len(tweet_scores) + 1)]
    line_chart.add('Compound score', tweet_scores)
    return line_chart.render_data_uri()
