import json
from decimal import Decimal


def to_serializable(val):
    if isinstance(val, Decimal):
        return str(val)
    return val


def generate_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps(body, default=to_serializable)
    }


def generate_error_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps(body, default=to_serializable)
    }
