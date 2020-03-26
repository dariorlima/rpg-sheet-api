from datetime import datetime

from rpg.response.json import send_json

code_dt = lambda: datetime.now().strftime('%d/%m/%Y %I:%M %p')

class HTTPCodes:
    def __init__(self, message, status_code, headers={}, item={}):
        self.response = send_json(
            {
                'status': message,
                'time': code_dt(),
                'item': item
            },
            status_code,
            headers=headers
        )

Success = lambda message='Success', headers={}, item={}: HTTPCodes(
    message, 200, headers=headers, item=item).response

Bad = lambda message='Bad request', headers={}, item={}: HTTPCodes(
    message, 400, headers=headers, item=item).response

Unauthorized = lambda message='Unauthorized', headers={}, item={}: HTTPCodes(
    message, 401, headers=headers, item=item).response