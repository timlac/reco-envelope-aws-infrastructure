import os
from utils import generate_response
from group_list_repository import GroupListRepository


def handler(event, context):

    group_list_id = event['pathParameters']['group_list_id']

    print(f"group_list_id: {group_list_id}")

    try:
        group_list_repository = GroupListRepository(os.environ["DYNAMODB_TABLE_NAME"])
        resp = group_list_repository.get_list(group_list_id)

        print(f"resp: {resp}")

        return generate_response(200, body=resp)
    except Exception as e:
        return generate_response(500, body="Error inserting data {}".format(str(e)))
