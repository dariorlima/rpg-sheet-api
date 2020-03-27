import json
import os

import boto3
from boto3.dynamodb.conditions import Attr

from rpg.dynamodb.table import DynamodbTable
from rpg.response.codes import Success, Bad
from rpg.request.parser import parse_headers


characters_table = DynamodbTable.from_env('character_table_name')
client = boto3.client('kinesis')

def get_characters(path_params, headers):

    if 'character_id' in path_params:
        character_id = path_params['character_id']
        character = characters_table.get_item(Key={'id': character_id})

        if 'Item' not in character:
            return Bad()

        character = character['Item']
       
        
        return Success(item=character)

    characters = characters_table.scan()['Items']
    
    jsonString = json.dumps(characters, separators=(',', ':'))
    
    response = client.put_record(
        StreamName='rpg-sheet-data-stream',
        Data=jsonString.encode(),
        PartitionKey="123456789"
    )
    
    return Success(item=characters)


def handler(event, context):

    headers = parse_headers(event['headers'])
    path_params = event['pathParameters'] or {}

    return get_characters(path_params, headers)

