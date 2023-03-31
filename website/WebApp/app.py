from flask import Flask, render_template

import requests

app = Flask(__name__)

@app.route("/records")
def records():
    response = requests.get("http://localhost:7071/records")
    records = response.json()
    return render_template("records.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)