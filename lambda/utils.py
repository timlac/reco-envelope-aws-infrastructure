import json
from decimal import Decimal
import hashlib
import uuid

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


def generate_id():
    # Generate a random UUID
    unique_uuid = uuid.uuid4()
    # Convert the UUID to a string
    uuid_str = str(unique_uuid)
    # Create a hash object using the hashlib library (you can choose a different algorithm)
    hash_object = hashlib.sha256()
    # Update the hash object with the UUID string
    hash_object.update(uuid_str.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    unique_hash = hash_object.hexdigest()
    return unique_hash