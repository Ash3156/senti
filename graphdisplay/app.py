from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
from random import seed
from random import random

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


                
colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"

]


@app.route('/api/data')
@cross_origin()
def data():
    values = []
    for i in range(3):
        values.append([])
        values[i].append([])
        values[i].append([])
        for _ in range(6):
            values[i][0].append(15000*random())
            values[i][1].append(15000*random())
    labels = [6,5,4,3,2,1]
    _max = 17000

    return jsonify({'labels': [str(i) for i in labels], 'max': _max, 'values': values})

@app.route('/')
def line():

    return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', values=[], max=1700, labels=[])

@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)





















