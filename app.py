from flask import Flask, render_template, url_for
import json

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    with open(".\\result.json", 'r', encoding='utf-8') as outfile:
        articles = list(json.load(outfile).items())
    return render_template('index.html', articles=articles)


@app.route('/dividends')
def dividends():
    with open(".\\dividends.json", 'r', encoding='utf-8') as outfile:
        articles = list(json.load(outfile).items())
    return render_template('dividends.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)
