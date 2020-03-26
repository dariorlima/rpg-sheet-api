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

def put_character(character, headers, path_params):
    
    if 'character_id' not in path_params:
        return Bad()

    if 'id' in character:
        del character['id']

    character_id = path_params['character_id']
    _character = characters_table.get_item(Key={'id': character_id})
    
    if 'Item' not in _character:
        return Bad()

    _character = _character['Item']
    _character.update(character)

    characters_table.put_item(Item=character)
    
    return Success(item=character)

def handler(event, context):

    headers = parse_headers(event['headers'])
    character = json.loads(event['body'])
    path_params = event['pathParameters'] or {}

    return put_character(character, headers, path_params)

