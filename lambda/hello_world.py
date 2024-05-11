
from utils import generate_response


def handler(event, context):
    try:
        return generate_response(200, body="hello world")
    except Exception as e:
        return generate_response(500, body="Error generating list {}".format(str(e)))









