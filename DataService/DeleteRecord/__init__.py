#DeleteRecord
# Author: Anthony Santos
import logging

import json

from bson import json_util

import azure.functions as func

import data_manager



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.params.get('query')
            req_body = json.loads(req_body)
            res = data_manager.delete(req_body)
            if res is True:
                return func.HttpResponse(f"Record(s) deleted successfully: {res}", status_code=200)
            else:
                return func.HttpResponse(f"Error deleting record(s): {str(ValueError)}", status_code=400)
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
