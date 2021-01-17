from flask import Flask,render_template
from random import seed
from random import random

app = Flask(__name__)


                
colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route('/')
def line():
    values = []
    labels=[]
    for i in range(3):
        values.append([])
        for j in range(6):
            values[i].append(15000*random())
    labels= [6,5,4,3,2,1]
    line_labels=labels
    line_values=values

    return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels, values=line_values)























