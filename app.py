from flask import Flask, render_template, abort
import csv

app = Flask(__name__)

def load_data(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # pairs: (desc, value)
            pairs = [{"desc": row[i], "value": row[i+1]} for i in range(0, len(row), 2)]
            data.append(pairs)
    return data

# For demo, static and pricing use same csv structure
STATIC_DB = {'FR0000123456': load_data('data/isin_rows.csv')}
PRICING_DB = {'ABCX': load_data('data/isin_rows.csv')}
PRICES_DB = {'ABCX': [{'date': '2025-11-30', 'price': 102.34, 'sensi': 0.12}]}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<isin>")
def static_view(isin):
    rows = STATIC_DB.get(isin)
    if not rows:
        abort(404)
    return render_template("static.html", isin=isin, rows=rows)

@app.route("/pricing/<mic>")
def pricing_view(mic):
    rows = PRICING_DB.get(mic)
    if not rows:
        abort(404)
    return render_template("pricing.html", mic=mic, rows=rows)

@app.route("/prices/<mic>")
def prices_view(mic):
    prices_data = PRICES_DB.get(mic)
    if not prices_data:
        abort(404)
    return render_template("prices.html", mic=mic, prices=prices_data)

if __name__ == "__main__":
    app.run(debug=True)