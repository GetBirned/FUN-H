from flask import Flask, render_template, redirect, url_for, request
import requests
import json

app = Flask(__name__)


read_record_url = 'https://testfunctionappcs518.azurewebsites.net/api/readrecords'
create_record_url = 'https://testfunctionappcs518.azurewebsites.net/api/createrecord'



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/ReadRecords/')
def readRecords():
    response = requests.get(read_record_url, params={"query": '{}'})
    records = json.loads(response.text)
    return render_template('records.html', records=records)

@app.route('/CreateRecords', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        field1 = request.form['field1']
        field2 = request.form['field2']
        field3 = request.form['field3']

        response = requests.post(create_record_url, json={'food': field1, 'calories': field2, 'meal': field3})
        if response.status_code == 200:
            # Redirect to view all records
            return redirect(url_for('view_all_records'))
        else:
            # Handle errors in creating the record
            return "Error creating record. Please try again."

@app.route('/view_all_records')
def view_all_records():
    return redirect(url_for('readRecords'))

if __name__ == '__main__':
    app.run()
