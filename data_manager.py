import pymongo
import sys
"""
This is a reST style.

:param param_1: this is the first parameter
:param param_2: this is the second parameter
:returns: this is a description of what is returned
:raises keyError: raises an exception

"""

# use a global variable to store your collection object
mycol = None


"""
Connect to the local MongoDB server, database, and collection.

"""
def initialize():
    # specify that we are using the global variable mycol
    global mycol
    
    # connect to your local mongoDB server
    my_client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)

    # check for a successful connection
    try:
        my_client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Connection timed out, please check if your mongod is running!")
        sys.exit(1)

    mydata = my_client["mydatabase1"]
    mycol = mydata["mycollection1"]

"""
Drop the collection and reset global variable mycol to None.

"""
def reset():
    # specify that we are using the global variable mycol
    global mycol
    if mycol != None:
      delete({})
      mycol.drop()
      mycol = None



"""
Insert document(s) into the collection.

:param document: a Python list of the document(s) to insert
:returns: result of the operation

"""
def create(document):
    global mycol
    if mycol == None:
       initialize()
    x = []
    if len(document) > 1:
        x = mycol.insert_many(document)
    else:
        x = mycol.insert_one(document)
    return x

    
    

"""
Retrieve document(s) from the collection that match the query,
if parameter one is True, retrieve the first matched document,
else retrieve all matched documents.

:param query: a Python dictionary for the query
:param one: an indicator of how many matched documents to be retrieved, by default its value is False
:returns: all matched document(s)

"""
def read(query, one=False):
  global mycol

  if one:
    return mycol.find_one(query)
  cursor = mycol.find(query)
  documents = []
  for doc in cursor: 
    documents.append(doc) 
  return documents



"""
Update document(s) that match the query in the collection with new values.

:param query: a Python dictionary for the query
:param new_values: a Python dictionary with updated data fields / values
:returns: result of the operation

"""
def update(query, new_values):
  global mycol
  return mycol.update_many(query, new_values) 


"""
Remove document(s) from the collection that match the query.

:param query: a Python dictionary for the query
:returns: result of the operation

"""
def delete(query):
  global mycol
  return mycol.delete_many(query)






if __name__ == "__main__":
  # sample tests
  initialize()

  for i in range(0, 50):
    create({'value': i})

  print("Inserted values:")
  for doc in read({}):
    print(doc)
  
  # delete specific value
  delete({'value': { '$gt': 5}})
  # check if deleted
  if mycol.count_documents({}) == 6:
    print("Correctly deleted.")
    print("Inserted values:")
    for doc in read({}):
      print(doc)

    print("Updating values:")
    update({'value': {'$lte': 5}}, {'$set': {'value': 'woah!'}})
    for doc in read({}):
      print(doc)

    delete({})
    if mycol.count_documents({}) == 0:
      print("Collection is empty! Passing test")
    else:
      print("Collection is not empty. Failing test")

  else:
    print("Failed to delete items greater than 5!")
    for doc in read({}):
       print(doc)

  reset()

  # clear db

  

