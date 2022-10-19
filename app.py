import form
import twitter

from datetime import datetime

from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        try:
            name, range_or_amount_from, from_date, date_or_amount = form.parse_form(request.form)
        except form.Error:
            return 'Invalid data in form.', 400

        try:
            id = twitter.get_twitter_id(name)
        except twitter.Error:
            return 'Invalid username.', 400

        if range_or_amount_from == 'range':
            tweets = twitter.get_tweets(
                id=id,
                from_date=from_date,
                until_date=date_or_amount)
        else:
            tweets = twitter.get_tweets(
                id=id,
                from_date=from_date,
                max_results=date_or_amount)

        translated_tweets = twitter.translate_tweets(tweets)
        scores_tweets = twitter.analyze_tweets(translated_tweets)
        graph = twitter.plot_tweets(scores_tweets)
        return render_template('index.html', graph=graph)
