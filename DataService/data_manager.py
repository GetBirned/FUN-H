import pymongo
import sys
import unittest
import logging
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

    #########################
    # INSERT YOU CODE BELOW #
    #########################

   # connect to your local mongoDB server
# auth_str = "AnthonySantos:9V34IYo7pDZYKyoS"
# conn_url = "clustercs518anthonysant.entwzds.mongodb.net/api"
# conn_str = f"mongodb+srv://{auth_str}@{conn_url}"
my_client = pymongo.MongoClient(
    "mongodb+srv://AnthonySantos:9V34IYo7pDZYKyoS@clustercs518anthonysant.entwzds.mongodb.net/?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)

# check for a successful connection
try:
    my_client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
    print("Connection timed out, please check if your mongod is running!")
    sys.exit(1)

# create a database named 'mydatabase'
my_database = my_client["mydatabase"]

# Note that a database doesn't get created until it gets content
# create a collection named 'mycollection'
# Note that a collection doesn't get created until it gets content
mycol = my_database['mycollection']

"""
Drop the collection and reset global variable mycol to None.

"""


def reset():
    # specify that we are using the global variable mycol
    global mycol

    #########################
    # INSERT YOU CODE BELOW #
    #########################
    # Drops the collection, deletes all documents

    # Don't know why the drop function isn't working like this
    # TA's told me to leave it out
    mycol.drop()
    mycol = None


"""
Insert document(s) into the collection.

:param document: a Python list of the document(s) to insert
:returns: result of the operation

"""


def create(document):
    #########################
    # INSERT YOU CODE BELOW #
    #########################
    x = 0
    try:
        x = mycol.insert_many(document)
    except:
        x = mycol.insert_one(document)
    # Should probably wrap in try and catch statements instead
    if x == 0:
        return "False"
    else:
        return "True"


"""
Retrieve document(s) from the collection that match the query,
if parameter one is True, retrieve the first matched document,
else retrieve all matched documents.

:param query: a Python dictionary for the query
:param one: an indicator of how many matched documents to be retrieved, by default its value is False
:returns: all matched document(s)

"""


def read(query, one=False):
    #########################
    # INSERT YOU CODE BELOW #
    #########################

    if one == True:
        return mycol.find_one(query)
    else:
        c = mycol.find(query)
        return list(c)


"""
Update document(s) that match the query in the collection with new values.

:param query: a Python dictionary for the query
:param new_values: a Python dictionary with updated data fields / values
:returns: result of the operation

"""


def update(query, new_values):
    #########################
    # INSERT YOU CODE BELOW #
    #########################

    x = mycol.update_many(query, {'$set': new_values})
    if x == 0:
        return "False"
    else:
        return "True"


"""
Remove document(s) from the collection that match the query.

:param query: a Python dictionary for the query
:returns: result of the operation

"""


def delete(query):
    #########################
    # INSERT YOU CODE BELOW #
    #########################

    x = mycol.delete_many(query)
    if x == 0:
        return "False"
    else:
        return "True"


if __name__ == "__main__":
    # sample tests
    initialize()
    # reset()

    print("Testing Create and Read")
    create({'title': 'test', 'message': "testing 1 2"})
    doc = read({}, one=True)
    print(doc)

    print("Testing Update")
    update({'title': 'test'}, {'message': "testing 3 4"})
    doc = read({}, one=True)
    print(doc)

    print("Testing Delete")
    delete({'title': 'test'})
    doc = read({}, one=True)
    print(doc)

    reset()

    #########################
    # INSERT YOU TESTS BELOW #
    #########################
    initialize()
    mydict = [{"First Name": "Anthony", "Last Name": "Santos", "Age": 19},
              {"First Name": "John", "Last Name": "Doe", "Age": 19},
              {"First Name": "Dr.", "Last Name": "Bob", "Age": 65},
              ]
    print("Testing create and read 2")
    create(mydict)
    doc0 = read({})
    print(*doc0, sep="\n")

    print("Testing update 2")
    check = update({"Age": 19}, {"Age": 21})
    doc1 = read({"Age": 19}, one=False)
    doc2 = read({"Age": 21}, one=False)
    if check:
        # Should be no items in doc1
        print(doc1)
        print(*doc2, sep="\n")
    print("Testing Delete 2")
    delete({"Age": 19})
    doc3 = read({}, one=False)
    # Should print all because there are noo age 19 after update
    print(*doc3, sep="\n")
    print()
    delete({"Age": 21})
    doc4 = read({}, one=False)
    # Should just print the age 65
    print(*doc4, sep="\n")
    # Delete remaining of documents
    delete({})
    doc5 = read({}, one=False)
    # Should print nothing
    print(*doc5, sep="\n")
    reset()
