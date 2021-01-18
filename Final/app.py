from flask import Flask, render_template, request, jsonify, redirect

from flask_cors import CORS, cross_origin
from random import seed
from random import random

import functions as f

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"

]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST', 'GET'])
def redirect_to_display():
    query=request.form.get("query")
    query=query.split()
    query="%20".join(query)
    return redirect("/search/"+query)

@app.route('/search/<query>', methods=['POST', 'GET'])
def show_results(query):
    query = query.split("%20")
    query = " ".join(query)
    query_results = f.add_sentiments(f.full_results(f.search_url(query)), False)
    return render_template("display.html", query_results = query_results)



# for the global data charts
@app.route('/api/data')
@cross_origin()
def data():
    values = []
    for i in range(8):
        values.append([])
        values[i].append([])
        values[i].append([])
        for _ in range(6):
            values[i][0].append(1*random())
            values[i][1].append(1*random())
    labels = [6,5,4,3,2,1]
    _max = 1.2

    return jsonify({'labels': [str(i) for i in labels], 'max': _max, 'values': values})

@app.route('/trends', methods=['GET'])
def line():
    return render_template('trends.html', title='Polarity and Subjectivity By Country')

if __name__ == '__main__':
    app.run(debug=True)
