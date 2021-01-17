from flask import Flask, render_template, request, jsonify, redirect
# import time
# import random
# from tempfile import mkdtemp


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST', 'GET'])
def print_results():
    query=request.form.get("query")
    query=query.split()
    query="%20".join(query)
    return redirect("/search/"+query)

@app.route('/search/<query>', methods=['POST', 'GET'])
def show_results(query):
    query=query.split("%20")
    query=" ".join(query)
    return render_template("display.html", query=query)

if __name__ == '__main__':
    app.run(debug=True)
