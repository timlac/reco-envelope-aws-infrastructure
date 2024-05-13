import json
import os
from utils import generate_response, generate_id
from group_list_repository import GroupListRepository
from models import GroupListModel, GroupListItemModel


def handler(event, context):
    data = json.loads(event["body"])

    group_list_items = []

    for item in data:
        item_model = GroupListItemModel(retrieved=0, data=item)
        group_list_items.append(item_model)

    group_list_id = generate_id()

    model = GroupListModel(group_list_id=group_list_id,
                           group_list_items=group_list_items)

    try:
        group_list_repository = GroupListRepository(os.environ["DYNAMODB_TABLE_NAME"])
        resp = group_list_repository.create_list(model)

        return generate_response(200, body=resp)
    except Exception as e:
        return generate_response(500, body="Error inserting data {}".format(str(e)))
