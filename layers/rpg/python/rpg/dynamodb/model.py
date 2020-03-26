from boto3.dynamodb.conditions import Attr

from rpg.dynamodb.table import DynamodbTable


class BaseModel:
    def __init__(self, table_name, schema={}):
        self.__table = DynamodbTable(table_name)
        self.__before_get_actions = {}
        self.schema = schema

    def __apply_schema_fields(self, schema):
        if isinstance(schema, dict):
            for k, v in schema.items():
                schema[k] = self.__apply_schema_fields(v)
        
        if hasattr(schema, '__call__'):
            return schema()
        
        return schema

    def __update_schema(self, schema, item):
        for k, v in schema.items():
            if k in item:
                if isinstance(v, dict):
                    schema[k] = self.__update_schema(schema[k], item[k])
                
                else:
                    schema[k] = item[k]

        return schema

    def __apply_schema(self, item):
        schema_copy = self.schema.copy()
        schema_copy = self.__apply_schema_fields(schema_copy)        
        item = self.__update_schema(schema_copy, item)
        return item

    def define_before_get(self, action_list):
        self.before_get_actions = action_list

    def get(self, query={}):
        expr = None

        for k, v in query.items():
            if expr == None:
                expr = Attr(k).eq(v)
            else:
                expr = expr & Attr(k).eq(v)

        data = self.__table.scan(FilterExpression=expr)['Items']

        for i, item in enumerate(data):
            for k, v in item.items():
                if k in self.__before_get_actions:
                    item[k] = self.__before_get_actions[k](v)

            data[i] = item
        
        return data

    def get_one(self, key, value):
        item = self.__table.get_item(Key={key: value})

        if 'Item' not in item:
            return None
        
        item = item['Item']

        for k, v in item.items():
            if k in self.__before_get_actions:
                item[k] = self.__before_get_actions(v)
        
        return item
    
    def insert(self, data):
        data = list(map(lambda item: self.__apply_schema(item)))

        with self.__table.batch_writer() as batch:
            for item in data:
                batch.put_item(Item=item)

    def insert_one(self, item):
        item = self.__apply_schema(item)
        self.__table.put_item(Item=item)
        return item

    def delete(self, query_list):
        with self.__table.batch_writer() as batch:
            for query in query_list:
                batch.delete_item(Key=query)

    def delete_one(self, key, value):
        return self.__table.delete_item(Key={key: value})