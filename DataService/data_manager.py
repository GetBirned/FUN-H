import sys
import pymongo
from pymongo.errors import ConnectionFailure
import logging
from bson import ObjectId
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
    # connect to your local mongoDB server UDOYKIcm000bL8uF
    # ssl=True
    my_client = pymongo.MongoClient("mongodb+srv://AnthonySantos:UDOYKIcm000bL8uF@clustercs518.olluvi6.mongodb.net/?retryWrites=true&w=majority", serverSelectionTimeoutMS=12500)

    # check for a successful connection
    try:
        my_client.admin.command('ismaster')
    except ConnectionFailure:
        print("Server unavailable")
        sys.exit(1)
    # try:
    #     my_client.server_info()
    # except pymongo.errors.ServerSelectionTimeoutError as err:
    #     print("Connection timed out, please check if your mongod is running!")
    #     sys.exit(1)

    mydata = my_client["mydatabase"]
    mycol = mydata["mycollection"]

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
    if isinstance(document, list):
        result = mycol.insert_many(document)
    else:
        result = mycol.insert_one(document)
    
    if result.acknowledged:
        return True
    else:
        return False


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
    if query is None:
        c = mycol.find()
        return list(c)
    if one is True:
        return mycol.find_one(query)
    else:
        try: 
            temp = query
            temp = str(temp['_id'])
            x = mycol.find_one({"_id": ObjectId(temp)})
            if x != None:
                return x
        except:
            pass
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
    try: 
        temp = query
        temp = str(temp['_id'])
        x = mycol.update_many({"_id": ObjectId(temp)}, {'$set': new_values})
        if x != 0:
            return True
    except:
        pass
    x = mycol.update_many(query, {'$set': new_values})
    if x == 0:
        return False
    else:
        return True


"""
Remove document(s) from the collection that match the query.

:param query: a Python dictionary for the query
:returns: result of the operation

"""


def delete(query):
    #########################
    # INSERT YOU CODE BELOW #
    #########################
    # x = mycol.delete_many(query)
    # if x == 0:
    #     return False
    # else:
    #     return True
    try: 
        temp = query
        temp = str(temp['_id'])
        x = mycol.delete_many({"_id": ObjectId(temp)})
        if x.deleted_count != 0:
            return True
    except:
        pass
    
    try:
        x = mycol.delete_many(query)
        if x.deleted_count == 0:
            return False
        else:
            return True
    except Exception as e:
        return False


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
