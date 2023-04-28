from flask import Flask, jsonify, request, session, redirect
import requests
import json
# Hashing to encrypt password
from passlib.hash import pbkdf2_sha256
import uuid

class User:
    # Create a session using Flask's framework
    def start_session(self, user):
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user)
    
    # Sign up for account
    def signup(self):
        # Create user object
        user = {
            # Generates a new hex as an id
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        print(type(user))
        
        # Encrypt password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        # Check if email already exists
        print(requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{"email": "'+user['email']+'"}'}))
        if requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{"email": "'+user['email']+'"}'}):
            return jsonify({"error":"Email address already in use"}), 400
        # Attempt to create account
        if requests.post('https://testfunctionappcs518.azurewebsites.net/api/createrecord', json=user):
            return self.start_session(user)
        # Failed creating account
        return jsonify({"error": "Account Creation Failed"}), 400
    
    # Signout of account / session
    def signout(self):
        session.clear()
        return redirect('/')
    
    # Log in user
    def login(self):
        user = requests.get("https://testfunctionappcs518.azurewebsites.net/api/readrecords", params={"query":'{"email": "'+request.form.get("email")+'"}'})
        # Checks if user was found and that password is correct
        if user and pbkdf2_sha256.verify(request.form.get('password'), json.loads(user.text)[0]["password"]):
            # Have to make a new user dictionary because the user type we get is a response
            # user.text gives us a string, the using json.loads gives us a list
            # Easiest this way to make a new dictionary and copy over the values
            user2 = {
            "_id": json.loads(user.text)[0]["_id"],
            "name": json.loads(user.text)[0]["name"],
            "email": json.loads(user.text)[0]["email"],
            "password": json.loads(user.text)[0]["password"]
            }
            return self.start_session(user2)
        
        return jsonify({ "error": "Invalid Login Credentials"}), 401
    
    # Delete an account
    def delete(self):
        # Get user details through session
        user = session['user']
        query = user["_id"]
        print(query)
        session.clear()
        x = requests.get("https://testfunctionappcs518.azurewebsites.net/api/deleterecord", params={'query': '{"_id": "'+str(query)+'"}'})
        if x.status_code == 200:
            return redirect('/')
        else:
            return redirect('/userplates')