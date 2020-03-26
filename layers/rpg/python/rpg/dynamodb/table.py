import os
import decimal

import boto3


class DynamodbTable:
    def __init__(self, table_name):
        dynamodb = self.__get_dynamodb()
        self.table = dynamodb.Table(table_name)

    def __getattr__(self, attr):
        if hasattr(self.table, attr):
            return getattr(self.table, attr) if (
                not hasattr(self, f'__{attr}')) else getattr(self, f'__{attr}')
        
        raise AttributeError(f'Attribute {attr} does not exists in DynamodbTable.')

    def __get_dynamodb(self):
        boto3_kwargs = {}
        
        if 'AWS_SAM_LOCAL' in os.environ and os.environ['AWS_SAM_LOCAL'] == 'true':
            boto3_kwargs['endpoint_url'] = 'http://ddb:8000'
            boto3_kwargs['region_name'] = 'eu-west-1'

        return boto3.resource('dynamodb', **boto3_kwargs)

    def __put_item(self, Item={}, **kwargs):
        d = {}
        for k, v in Item.items():
            d[k] = v if type(v) != float else decimal.Decimal(v)
        
        return self.table.put_item(Item=d, **kwargs)

    @staticmethod
    def from_env(envvar):
        if envvar not in os.environ:
            raise KeyError(f'Variable {envvar} not found in environment.')

        return DynamodbTable(os.environ[envvar])