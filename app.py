import form
import twitter

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

# Met extra uitleg comments

@app.route("/", methods=('GET', 'POST'))
def index():
    # Render de homepagina template als er een get request gedaan wordt.
    if request.method == 'GET':
        return render_template('index.html')

    # Render de homepagina met de grafiek als er een post request gedaan wordt.
    if request.method == 'POST':
        # Probeer het formulier in te lezen en geef een error terug als het niet lukt.
        try:
            name, range_or_amount_from, from_date, date_or_amount, show_tweets = form.parse_form(
                request.form)
        except form.Error:
            return 'Invalid data in form.', 400

        # Probeer de twitter id van een gebruikersnaam op te halen en geeft een error terug als het niet lukt.
        try:
            id = twitter.get_twitter_id(name)
        except twitter.Error:
            return 'Invalid username.', 400

        # Haal tweets op op basis van "period" of "from a date"
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

        # Vertaal tweets
        translated_tweets = twitter.translate_tweets(tweets)

        # Bereken de scores van de tweets.
        scores_tweets = twitter.analyze_tweets(translated_tweets)

        # Als "show_tweets" niet aan staat laat dan de grafiek zien, laat anders de tekst van de tweets zien.
        if not show_tweets:
            graph = twitter.plot_tweets(scores_tweets)
            return render_template(
                'index_graph.html',
                graph=graph)
        else:
            tweets_and_scores = zip(tweets[:8], scores_tweets[:8])
            return render_template(
                'index_tweets.html',
                tweets=tweets_and_scores)
