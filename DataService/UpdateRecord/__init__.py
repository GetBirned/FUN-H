#UpdateRecord
# Author: Anthony Santos
import logging

import json

from bson import json_util

import azure.functions as func

import data_manager


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    data_manager.initialize()
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.params.get('query')
            # logging.info(f"CHECK1 {req_body}")
            req_body = json.loads(req_body)
            # logging.info(f"CHECK2 {req_body}")
            req_body2 = req.params.get('new_value')
            # logging.info(f"CHECK3 {req_body2}")
            # print("AAAA")
            req_body2 = json.loads(req_body2)
            # print("BBBB")
            # logging.info(f"CHECK4 {req_body2}")
            res = data_manager.update(req_body, req_body2)
            # logging.info(f"CHECK5 {res}")
            if not res:
                return func.HttpResponse("Failed to Update Record", status_code=400)
            else:
                return func.HttpResponse(f"Record(s) updated successfully: {res}", status_code=200)
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
