import logging
import json

import azure.functions as func


# Import helper script
from .predict import predict_image_from_url

def main(req: func.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get('img')
    top = 20
    try:
        top = int(req.params.get('top'))
    except:
        pass
    logging.info('Image URL received: ' + image_url)
    logging.info('with top n: ' + str(top))
    results = predict_image_from_url(image_url, top)

    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    return func.HttpResponse(json.dumps(results), headers = headers)
