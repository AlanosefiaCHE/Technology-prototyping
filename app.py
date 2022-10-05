from dataclasses import dataclass
from flask import Flask, render_template, request
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json

app = Flask(__name__)

messages = [
    {'title': "Message one", 'content': "Message one content"},
    {'title': "Message two", 'content': "Message two content"}
]


@app.route('/')
def index():
    tweets = get_tweets()
    for tweet in tweets:
        analyze_tweet(tweet)

    return render_template('display.html', messages=messages)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content']:
            return

        messages.append(
            {'title': request.form['title'], 'content': request.form['content']})

    return render_template('form.html')


def analyze_tweet(tweet_text):
    ss_list = []
    for sentence in nltk.sent_tokenize(tweet_text):
        sid = SentimentIntensityAnalyzer()
        ss_list.append(sid.polarity_scores(sentence))

    ss = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
    for e in ss_list:
        ss['neg'] += e['neg']
        ss['neu'] += e['neu']
        ss['pos'] += e['pos']
        ss['compound'] += e['compound']

    for k in ss:
        ss[k] /= len(ss)

    print(ss)


def get_tweets():
    with open('example_tweets.json', 'r') as f:
        return json.load(f)['tweets']
