from flask import Flask, render_template, request, jsonify, redirect
import functions as f

app = Flask(__name__)

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

@app.route('/trends', methods=['GET'])
def trends():
    return render_template("trends.html")

if __name__ == '__main__':
    app.run(debug=True)
