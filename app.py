from datetime import datetime

import deep_translator
import nltk
import pygal
import tweepy

from flask import Flask, render_template, request, make_response
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)

FORM_DATE_STRING = '%Y-%m-%d'

CLIENT = tweepy.Client(
    'AAAAAAAAAAAAAAAAAAAAAG9EhAEAAAAA%2BLR%2BJ1%2FpM0UC5y9QfHxPND7ccAI%3DvHGlimS0Gz93SWTqFglsr2J3PkYGUfLd7S7czHwsXyRMww8dNZ',
    return_type=dict)

SID = SentimentIntensityAnalyzer()


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        form = request.form

        id = CLIENT.get_users(usernames=[form['name']])['data'][0]['id']
        from_date = datetime.strptime(form['from'], FORM_DATE_STRING)

        if form['rangeOrAmountFrom'] == 'range':
            until_date = datetime.strptime(form['until'], FORM_DATE_STRING)
            tweets = get_tweets(id=id, from_date=from_date, until_date=until_date)
        elif form['rangeOrAmountFrom'] == 'amountFrom':
            tweets = get_tweets(id=id, max_results=int(form['amount']), from_date=from_date)
        else:
            return 'Invalid option selected', 400

        translated_tweets = translate_tweets(tweets)
        scores_tweets = analyze_tweets(translated_tweets)
        graph = plot_tweets(scores_tweets)
        return render_template('index.html', graph=graph)


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
    # TODO: Disable js.
    line_chart = pygal.Line(show_legend=False, js=[''])
    line_chart.add('Compound score', tweet_scores)

    line_chart.y_labels = [-1, -0.05, 0, 0.05, 1]
    line_chart.x_labels = [*range(1, len(tweet_scores) + 1)]

    return line_chart.render_data_uri()
