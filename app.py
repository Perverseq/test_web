from flask import Flask, render_template, url_for
import json


def render_articles(file, page):
    with open(file, 'r', encoding='utf-8') as outfile:
        articles = list(json.load(outfile).items())
    return render_template(page, articles=articles)


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_articles(".\\result.json", 'index.html')


@app.route('/dividends')
def dividends():
    return render_articles(".\\dividends.json", 'dividends.html')


if __name__ == '__main__':
    app.run(debug=True)
