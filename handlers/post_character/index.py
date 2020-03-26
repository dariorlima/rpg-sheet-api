import json
import os
import uuid
import time

import boto3
from boto3.dynamodb.conditions import Attr

from rpg.dynamodb.table import DynamodbTable
from rpg.response.codes import Success, Bad
from rpg.request.parser import parse_headers

characters_table = DynamodbTable.from_env('character_table_name')

def post_character(character, headers):
    
    character.update({
        'id': str(uuid.uuid4())
    })

    characters_table.put_item(Item=character)
    
    return Success(item=character)

def handler(event, context):

    headers = parse_headers(event['headers'])
    character = json.loads(event['body'])

    return post_character(character, headers)

