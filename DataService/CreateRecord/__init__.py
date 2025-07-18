# CreateRecord
# Author: Anthony Santos
import logging

import azure.functions as func

import data_manager

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')
    
    data_manager.initialize()

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            res = data_manager.create(req_body)
            if res is True:
                return func.HttpResponse(f"Record(s) created successfully: {res}", status_code=200)
            else:
                return func.HttpResponse(f"Error creating record(s): {str(ValueError)}", status_code=400)
        except ValueError:
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
