from flask import Flask, render_template, request

app = Flask(__name__)

messages = [
    {'title': "Message one", 'content': "Message one content"},
    {'title': "Message two", 'content': "Message two content"}
]


@app.route('/')
def index():
    return render_template('display.html', messages=messages)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content']:
            return

        messages.append(
            {'title': request.form['title'], 'content': request.form['content']})

    return render_template('form.html')
