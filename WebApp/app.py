from flask import Flask, render_template, url_for, request, redirect, send_file

import requests
from datetime import datetime
import json
from collections import defaultdict
from datetime import datetime
from bson import json_util, ObjectId

app = Flask(__name__)

@app.route('/image')
def serve_images():
    return send_file('./logoFUNH.png', mimetype='image/png')

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', url_create=url_for('create'), url_records=url_for('records'))

@app.route('/phillymenu', methods=["GET"])
def phillyMenu():
    current_time = datetime.now()
    date = ("%s-%s-%s" % (current_time.month, current_time.day, current_time.year))
    response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{"location": "philly", "date": "'+date+'"}'})
    records = json_util.loads(response.text)
    return render_template('phillyMenu.html', records=records, url_index=url_for('index'), url_records=url_for('records'), url_create=url_for('create'), url_hocoMenu=url_for('hocoMenu'))

@app.route('/hocomenu', methods=["GET"])
def hocoMenu():
    current_time = datetime.now()
    date = ("%s-%s-%s" % (current_time.month, current_time.day, current_time.year))
    response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{"location": "hoco", "date": "'+date+'"}'})
    records = json_util.loads(response.text)
    return render_template('hocoMenu.html', records=records, url_index=url_for('index'), url_records=url_for('records'), url_create=url_for('create'), url_phillyMenu=url_for('phillyMenu'))

@app.route('/contact', methods=["GET"])
def contact():
    return render_template('contact.html')
   

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
        return redirect(url_for('records'))
        # return render_template('create.html', url_index=url_index, url_records=url_records)
    elif request.method == "GET":
        return render_template('create.html', url_index=url_for('index'), url_records=url_for('records'), url_phillyMenu=url_for('phillyMenu'))

@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        query = request.args.get("query")
        firstName = request.form.get("first name")
        lastName = request.form.get("last name")
        age = request.form.get("age")
        doc = json.dumps({"First Name": firstName, "Last Name": lastName, "Age": age})
        requests.post('https://testfunctionappcs518.azurewebsites.net/api/updaterecord', params={"query": '{"_id": "'+str(query)+'"}', "new_value": doc})
        return redirect(url_for('records'))
    elif request.method == "GET":
        query = request.args.get("query")
        response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={'query': '{"_id": "'+str(query)+'"}'})
        record = json_util.loads(response.text)
        return render_template('edit.html', record=record, url_index=url_for('index'), url_records=url_for('records'), url_phillyMenu=url_for('phillyMenu'))

@app.route('/records', methods=["GET", "POST"])
def records():
    if request.method == "POST":
        query = request.form.get("query")
        #query = ObjectId(query)
        response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/deleterecord", params={'query': '{"_id": "'+str(query)+'"}'})
        response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{}'})
        records = json_util.loads(response.text)
        return render_template("records.html", records=records, url_index=url_for('index'), url_create=url_for('create'), url_phillyMenu=url_for('phillyMenu'))
    else:
        response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{}'})
        records = json_util.loads(response.text)
        return render_template("records.html", records=records, url_index=url_for('index'), url_create=url_for('create'), url_phillyMenu=url_for('phillyMenu'))


@app.route('/date', methods=["GET", "POST"])
def date():
    if request.method == "POST":
        selected_date = request.form.get("date")
        parsed_date = datetime.strptime(selected_date, "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%-m-%-d-%Y") # Updated line
        
        response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{"date": "'+formatted_date+'"}'})
        records = json_util.loads(response.text)

        sorted_records = {"philly": defaultdict(list), "hoco": defaultdict(list)}

        for record in records:
            if record["location"] == "philly":
                sorted_records["philly"][record["meal"]].append(record)
            elif record["location"] == "hoco":
                sorted_records["hoco"][record["meal"]].append(record)

        return render_template("date.html", records=sorted_records)
    else:
        return render_template("date.html")



if __name__ == "__main__":
    app.run(debug=True)
