import json

import deep_translator

from flask import Flask, render_template, request

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import matplotlib.pyplot as pyplot

import base64
from io import BytesIO

app = Flask(__name__)

sid = SentimentIntensityAnalyzer()


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('form.html')

    if request.method == 'POST':
        print(request.form)

        tweets = get_tweets()
        tweets_analysis = analyze_tweets(tweets)

        pyplot.ylim((-1.0, 1.0))
        pyplot.plot(tweets_analysis[0], label="neg")
        pyplot.plot(tweets_analysis[1], label="neu")
        pyplot.plot(tweets_analysis[2], label="pos")
        pyplot.plot(tweets_analysis[3], label="comp")

        pyplot.legend()
        pyplot.plot()

        tmpfile = BytesIO()
        pyplot.savefig(tmpfile, format='svg')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

        return render_template('display.html', graph=encoded)

    else:
        return


def analyze_tweets(tweets_text):
    # Reken het sentiment uit van alle tweets in de tweet_list
    # Maak lijsten met de scores op verschillende vlakken voor de tweets
    neg_scores_tweets = []
    neu_scores_tweets = []
    pos_scores_tweets = []
    cmp_scores_tweets = []

    # Loop door de lijst met tweets heen.
    for tweet in tweets_text:
        # Maak lijsten met de verschillende scores op verschillende vlakken voor de zinnen in de tweets
        neg_sentences = []
        neu_sentences = []
        pos_sentences = []
        cmp_sentences = []

        # Tokenize de tweet (splits de tweet op in zinnen)
        sentences = nltk.tokenize.sent_tokenize(tweet)

        # Loop door de lijst met alle zinnen van de tweet
        for sentence in sentences:
            # Bereken het sentiment van de zin
            ss = SentimentIntensityAnalyzer().polarity_scores(sentence)

            # Voeg de score van de zin toe aan de lijst met de scores voor de zinnen in de tweet
            neg_sentences.append(ss["neg"])
            neu_sentences.append(ss["neu"])
            pos_sentences.append(ss["pos"])
            cmp_sentences.append(ss["compound"])

        # Bereken het gemiddelde van de verschillende scores van de zinnen in een tweet en voeg deze toe aan de lijst van scores voor de tweets
        neg_scores_tweets.append(sum(neg_sentences) / len(neg_sentences))
        neu_scores_tweets.append(sum(neu_sentences) / len(neu_sentences))
        pos_scores_tweets.append(sum(pos_sentences) / len(pos_sentences))
        cmp_scores_tweets.append(sum(cmp_sentences) / len(cmp_sentences))

        return neg_sentences, neu_sentences, pos_sentences, cmp_sentences


def get_tweets():
    with open('example_tweets.json', 'r') as f:
        data = json.load(f)['tweets']

    return deep_translator.GoogleTranslator(
        source="auto", target="en").translate_batch(data)

# Weergeven: Grafiek, 3 selecties voor positief negatief en neutraal. Die dan daaronder tweets laten zien.
# Tweets weergeven met een bepaalde score range.
