import os

from flask import Flask, render_template, request, jsonify
import time
import random
from tempfile import mkdtemp


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/display', methods=['POST'])
def display():
    ticker = request.form.get("stock_inquiry")
    print(ticker)
    test_list = [{'image': 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/20190503-delish-pineapple-baked-salmon-horizontal-ehg-450-1557771120.jpg?crop=0.669xw:1.00xh;0.173xw,0&resize=640:*',
 'url': 'https://www.bloomberg.com/news/articles/2021-01-14/citroen-sm-tesla-roadster-moke-ugly-cars-that-are-fun-to-drive',
 'title': "check check",
 'polarity': 0.696969,
 'subjectivity': 4.20}, {'image': 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/20190503-delish-pineapple-baked-salmon-horizontal-ehg-450-1557771120.jpg?crop=0.669xw:1.00xh;0.173xw,0&resize=640:*',
 'url': 'https://www.bloomberg.com/news/articles/2021-01-14/citroen-sm-tesla-roadster-moke-ugly-cars-that-are-fun-to-drive',
 'title': "check check",
 'polarity': 0.696969,
 'subjectivity': 4.20}]
    print(test_list[0]['polarity'])
    return render_template("display.html", ticker=ticker, test_list=test_list)

if __name__ == 'main':
    app.run(debug=True)
