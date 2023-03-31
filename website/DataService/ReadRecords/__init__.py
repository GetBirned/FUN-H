#ReadRecords
# Author: Anthony Santos
import logging

import json

import azure.functions as func

import data_manager

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')
    
    data_manager.initialize()
    
    name = req.params.get('name')
    # return func.HttpResponse(f"Query is {name}", status_code=400)
    if not name:
        try:
            req_body = req.params.get('query')
            req_body = json.loads(req_body)
            res = data_manager.read(req_body, False)
            if not res:
                return func.HttpResponse("No values found", status_code=400)
            else:
                return func.HttpResponse(f"Query given is: {req_body}\nHere are the requested document(s): {res}", status_code=200)
        except ValueError and TypeError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
