from flask import Flask, render_template, url_for, request, redirect

import requests

from bson import json_util

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', url_create=url_for('create'), url_records=url_for('records'))

@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # could check for valid login here
        # will need to change data below in the future
        firstName = request.form.get("first name")
        lastName = request.form.get("last name")
        age = request.form.get("age")
        doc = {"First Name": firstName, "Last Name": lastName, "Age": age}
        requests.post('https://testfunctionappcs518.azurewebsites.net/api/createrecord', json=doc)
        return redirect(url_for('records'), url_index=url_for('index'), url_create=url_for('create'))
        # return render_template('create.html', url_index=url_index, url_records=url_records)
    elif request.method == "GET":
        return render_template('create.html', url_index=url_for('index'), url_records=url_for('records'))

@app.route('/records')
def records():
    response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{}'})
    records = json_util.loads(response.text)
    return render_template("records.html", records=records, url_index=url_for('index'), url_create=url_for('create'))

if __name__ == "__main__":
    app.run(debug=True)