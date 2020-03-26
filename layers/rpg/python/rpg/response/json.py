import decimal

import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o) if o != round(o) else int(o)
        return super(DecimalEncoder, self).default(o)


def send_json(body, status_code=200, headers={}):
    r = {
        'body': json.dumps(body, cls=DecimalEncoder),
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        }
    }

    r['headers'].update(headers)

    return r