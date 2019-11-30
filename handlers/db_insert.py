import db
import os
import json

from typing import Dict, Any


def handle_bucket_event(event: Dict[str, Any], context: object):
    for record in event['Records']:
        body = json.loads(record['body'])
        message = json.loads(body['Message'])
        s3_object = message['Records'][0]['s3']['object']

        db.insert_s3_object(s3_object)
