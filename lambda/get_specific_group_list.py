import os
from utils import generate_response
from group_list_repository import GroupListRepository
from models import GroupListModel

def handler(event, context):

    group_list_id = event['pathParameters']['group_list_id']
    query_params = event['queryStringParameters']

    # handle the fact that event['queryStringParameters'] evaluates to None if there are no query parameters
    if query_params:
        only_retrieved_str = query_params.get("only_retrieved", 0)
        only_retrieved = only_retrieved_str == '1'
    else:
        only_retrieved = False

    print(f"only_retrieved: {only_retrieved}")
    print(f"group_list_id: {group_list_id}")

    try:
        group_list_repository = GroupListRepository(os.environ["DYNAMODB_TABLE_NAME"])
        resp = group_list_repository.get_list(group_list_id)
        model = GroupListModel(**resp)

        if only_retrieved:
            model.group_list_items = [item for item in model.group_list_items if item.retrieved == 1]

        return generate_response(200, body=model.dict())
    except Exception as e:
        return generate_response(500, body="Error inserting data {}".format(str(e)))
