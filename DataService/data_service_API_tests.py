# Author: Anthony Santos
# Purpose: Test CreateRecord and ReadRecords

# https://www.w3schools.com/python/module_requests.asp
import requests

# url = 'https://testfunctionappcs518.azurewebsites.net/api/createrecord'
# document = {'title': 'test'}     # or whatever your data fields are
# x = requests.post(url, json=document)
# print("response text", x.text)
# print("response code", x.status_code)

# url = 'https://testfunctionappcs518.azurewebsites.net/api/readrecords'
# x = requests.get(url, params={"query":'{}'})
# print("response text", x.text)
# print("response code", x.status_code)

# MY OWN TESTS 

# Create tests
# url = 'https://testfunctionappcs518.azurewebsites.net/api/createrecord'
# document = {'title': 'test', 'message': 'testing 1', 'number': 19}
# document2 = {'title': 'test', 'message': 'testing 2', 'number': 19}
# x = requests.post(url, json=document)
# y = requests.post(url, json=document2)
# print("response text", x.text)
# print("response code", x.status_code)
# print("response text", y.text)
# print("response code", y.status_code)
# # Read tests
# url = 'https://testfunctionappcs518.azurewebsites.net/api/readrecords'
# x = requests.get(url, params={"query":'{"message":"testing 2"}'})
# print("response text", x.text)
# print("response code", x.status_code)

# # Keep previous documents
# # Create tests 2
# url = 'https://testfunctionappcs518.azurewebsites.net/api/createrecord'
# document = {'title': 'test', 'message': "testing 3", 'number': 19}
# document2 = {'title': 'test', 'message': "testing 4", 'number': 19}
# document3 = [{'title': 'test', 'message': "testing 5", 'number': 21},
#              {'title': 'test', 'message': "testing 6", 'number': 21},
#              {'title': 'test', 'message': "testing 7", 'number': 19},
#              {'title': 'test', 'message': "testing 8", 'number': 21},
#              {'title': 'test', 'message': "testing 9", 'number': 20}
#              ]
# x = requests.post(url, json=document)
# y = requests.post(url, json=document2)
# z = requests.post(url, json=document3)
# print("response text", x.text)
# print("response code", x.status_code)
# print("response text", y.text)
# print("response code", y.status_code)
# print("response text", z.text)
# print("response code", z.status_code)
# # Read tests 2
# url = 'https://testfunctionappcs518.azurewebsites.net/api/readrecords'
# x = requests.get(url, params={"query":'{"number": 21}'})
# print("response text", x.text)
# print("response code", x.status_code)

# x = requests.get(url, params={"query":'{"number": 19}'})
# print("response text", x.text)
# print("response code", x.status_code)

# x = requests.get(url, params={"query":'{"number": 20}'})
# print("response text", x.text)
# print("response code", x.status_code)


url = 'https://testfunctionappcs518.azurewebsites.net/api/createrecord'
document = [{"First Name": "Anthony", "Last Name": "Santos", "Age": 19},
              {"First Name": "John", "Last Name": "Doe", "Age": 19},
              {"First Name": "Dr.", "Last Name": "Bob", "Age": 66},
              {"First Name": "Jane", "Last Name": "Doe", "Age": 20},
              {"First Name": "Scarlett", "Last Name": "Johansson", "Age": 38},
              {"First Name": "Robert", "Last Name": "Downey Jr.", "Age": 58},
              {"First Name": "Christian", "Last Name": "Bale", "Age": 49},
              {"First Name": "Ryan", "Last Name": "Gosling", "Age": 42},
              {"First Name": "Dr.", "Last Name": "Bob", "Age": 65},
              {"First Name": "Mr.", "Last Name": "Clean", "Age": 65},
              {"First Name": "Tom", "Last Name": "Brady", "Age": 45},
              {"First Name": "James", "Last Name": "Dean", "Age": 67},
              ]
x = requests.post(url, json=document)
print("response text", x.text)
print("response code", x.status_code)
url = 'https://testfunctionappcs518.azurewebsites.net/api/readrecords'
x = requests.get(url, params={"query":'{}'})
print("response text", x.text)
print("response code", x.status_code)