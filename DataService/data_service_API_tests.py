# Author: Anthony Santos
# Purpose: Test CreateRecord and ReadRecords

# https://www.w3schools.com/python/module_requests.asp
import requests
import data_manager

# Remove/change the data_manager.initialize() and data_manager.delete() if for some reason this doesn't work because of different implementation

data_manager.initialize()
# My reset function in data_manager doesn't really work?, so I'm just using delete instead
# Need to delete previous documents used in previous tests or they will begin to stack up
# Could just leave {} inside empty for empty query, meaning it will delete all documents
# data_manager.delete({"title":"test"})

# doc3 = data_manager.read({"title":"test"}, False)
# print(*doc3, sep="\n")

url = 'mongodb+srv://AnthonySantos:9V34IYo7pDZYKyoS@clustercs518anthonysant.entwzds.mongodb.net/?retryWrites=true&w=majority/api/CreateRecord'
document = {'title': 'test'}     # or whatever your data fields are

x = requests.post(url, json=document)
print("response text", x.text)
print("response code", x.status_code)

url = 'mongodb+srv://AnthonySantos:9V34IYo7pDZYKyoS@clustercs518anthonysant.entwzds.mongodb.net/?retryWrites=true&w=majority/api/ReadRecords'
x = requests.get(url, params={"query":'{"title":"test"}'})
print("response text", x.text)
print("response code", x.status_code)

# MY OWN TESTS 

# Create tests
url = 'http://localhost:7071/api/CreateRecord'
document = {'title': 'test', 'message': 'testing 1', 'number': 19}
document2 = {'title': 'test', 'message': 'testing 2', 'number': 19}
x = requests.post(url, json=document)
y = requests.post(url, json=document2)
print("response text", x.text)
print("response code", x.status_code)
print("response text", y.text)
print("response code", y.status_code)
# Read tests
url = 'http://localhost:7071/api/ReadRecords'
x = requests.get(url, params={"query":'{"message":"testing 2"}'})
print("response text", x.text)
print("response code", x.status_code)

# Keep previous documents
# Create tests 2
url = 'http://localhost:7071/api/CreateRecord'
document = {'title': 'test', 'message': "testing 3", 'number': 19}
document2 = {'title': 'test', 'message': "testing 4", 'number': 19}
document3 = [{'title': 'test', 'message': "testing 5", 'number': 21},
             {'title': 'test', 'message': "testing 6", 'number': 21},
             {'title': 'test', 'message': "testing 7", 'number': 19},
             {'title': 'test', 'message': "testing 8", 'number': 21},
             {'title': 'test', 'message': "testing 9", 'number': 20}
             ]
x = requests.post(url, json=document)
y = requests.post(url, json=document2)
z = requests.post(url, json=document3)
print("response text", x.text)
print("response code", x.status_code)
print("response text", y.text)
print("response code", y.status_code)
print("response text", z.text)
print("response code", z.status_code)
# Read tests 2
url = 'http://localhost:7071/api/ReadRecords'
x = requests.get(url, params={"query":'{"number": 21}'})
print("response text", x.text)
print("response code", x.status_code)

x = requests.get(url, params={"query":'{"number": 19}'})
print("response text", x.text)
print("response code", x.status_code)

x = requests.get(url, params={"query":'{"number": 20}'})
print("response text", x.text)
print("response code", x.status_code)

data_manager.reset()