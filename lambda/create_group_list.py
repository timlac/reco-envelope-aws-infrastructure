import json
import os
from generate_list import generate_blocks
from utils import generate_response, generate_id
from list_repository import ListRepository
from models import GroupListModel, GroupListItemModel


def handler(event, context):
    data = json.loads(event["body"])

    group_list_items = []

    for item in data:
        item_model = GroupListItemModel(retrieved=0, data=data)
        group_list_items.append(item_model)

    group_list_id = generate_id()

    model = GroupListModel(group_list_id=group_list_id,
                           group_list_items=group_list_items)

    try:
        template_repo = ListRepository(os.environ["DYNAMODB_TABLE_NAME"])
        resp = template_repo.create_list(model)

        return generate_response(200, body=resp)
    except Exception as e:
        return generate_response(500, body="Error generating list {}".format(str(e)))
