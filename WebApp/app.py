from flask import Flask, render_template, url_for, request, redirect, send_file, session
from functools import wraps
import requests
from datetime import datetime
import json
from collections import defaultdict
from datetime import datetime
from bson import json_util, ObjectId

from user.models import User

app = Flask(__name__)
# Random secret key I made
app.secret_key = b'?J o\xaem\xa2\xb7\xdc\x996(\xaa\x97\xb4\x12'

# Decorators. Checks if someone is logged in
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect('/createAccount')
    return wrap

def signedout_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return redirect('/userplates')
        else:
            return f(*arg, **kwargs)
    return wrap

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route('/user/removeAccount')
def removeAccount():
    return User().delete()

@app.route('/image')
def serve_images():
    return send_file('./logoFUNH.png', mimetype='image/png')

@app.route('/css')
def serve_css():
    return send_file('./styles.css', mimetype='text/css')

@app.route('/normalizecss')
def serve_normalizecss():
    return send_file('./normalize.css', mimetype='text/css')

@app.route('/accountcss')
def serve_accountcss():
    return send_file('./AccountStyles.css', mimetype='text/css')

@app.route('/jquery')
def serve_jquery():
    return send_file('./js/jquery.js', mimetype='text/js')

@app.route('/scripts')
def serve_scripts():
    return send_file('./js/scripts.js', mimetype='text/js')

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createAccount')
@signedout_required
def createAccount():
    return render_template('createAccount.html')

@app.route('/userplates')
@login_required
def dashboard():
    return render_template('userplates.html')

@app.route('/phillymenu', methods=["GET"])
def phillyMenu():
    current_time = datetime.now()
    date = ("%s-%s-%s" % (current_time.month, current_time.day, current_time.year))
    response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{"location": "philly", "date": "'+date+'"}'})
    if response.status_code == 400:
        records = []
    else:
        records = json_util.loads(response.text)
    return render_template('phillyMenu.html', records=records)

@app.route('/hocomenu', methods=["GET"])
def hocoMenu():
    current_time = datetime.now()
    date = ("%s-%s-%s" % (current_time.month, current_time.day, current_time.year))
    response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{"location": "hoco", "date": "'+date+'"}'})
    if response.status_code == 400:
        records = []
    else:
        records = json_util.loads(response.text)
    return render_template('hocoMenu.html', records=records)

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
        return render_template('create.html')

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
        return render_template('edit.html', record=record)

@app.route('/records', methods=["GET", "POST"])
def records():
    if request.method == "POST":
        query = request.form.get("query")
        #query = ObjectId(query)
        response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/deleterecord", params={'query': '{"_id": "'+str(query)+'"}'})
        response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{}'})
        records = json_util.loads(response.text)
        return render_template("records.html", records=records)
    else:
        response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{}'})
        records = json_util.loads(response.text)
        return render_template("records.html", records=records)


@app.route('/date', methods=["GET", "POST"])
def date():
    if request.method == "POST":
        selected_date = request.form.get("date")
        parsed_date = datetime.strptime(selected_date, "%Y-%m-%d")
        formatted_date = f"{parsed_date.month}-{parsed_date.day}-{parsed_date.year}"  # Updated line
        response = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{"date": "'+formatted_date+'"}'})
        if response.status_code == 400:
            records = []
        else:
            records = json_util.loads(response.text)

        sorted_records = {"philly": defaultdict(list), "hoco": defaultdict(list)}

        for record in records:
            if record["location"] == "philly":
                sorted_records["philly"][record["meal"]].append(record)
            elif record["location"] == "hoco":
                sorted_records["hoco"][record["meal"]].append(record)

        return render_template("date.html", records=sorted_records)
    else:
        return render_template("date.html", records={"philly": defaultdict(list), "hoco": defaultdict(list)})



if __name__ == "__main__":
    app.run(debug=True)
