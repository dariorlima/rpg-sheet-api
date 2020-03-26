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

def delete_character(path_params, headers):

    if 'character_id' not in path_params:
        return Bad()

    character_id = path_params['character_id']

    characters_table.delete_item(Key = {
        'id': character_id
    })
    
    return Success()

def handler(event, context):

    headers = parse_headers(event['headers'])
    path_params = event['pathParameters'] or {}

    return delete_character(path_params, headers)

