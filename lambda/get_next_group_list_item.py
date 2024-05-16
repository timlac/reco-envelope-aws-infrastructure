import os
import datetime
from zoneinfo import ZoneInfo
import json
from utils import generate_response
from group_list_repository import GroupListRepository
from models import GroupListModel, GroupListItemModel


def get_next_item_index(group_list_model):
    next_item_index = None
    for index, item in enumerate(group_list_model.group_list_items):
        if item.retrieved == 0:
            next_item_index = index
            break
        elif item.retrieved == 1:
            continue
        else:
            raise ValueError(f"Something went wrong, retrieved attribute is not 1, or 0, it is: {item.retrieved}")
    return next_item_index


def handler(event, context):
    group_list_id = event['pathParameters']['group_list_id']

    body = json.loads(event['body'])
    participant_id = body['participant_id']

    print(f"group_list_id: {group_list_id}")
    print(f"participant_id: {participant_id}")

    try:
        group_list_repository = GroupListRepository(os.environ["DYNAMODB_TABLE_NAME"])
        resp = group_list_repository.get_list(group_list_id)

        print(f"resp: {resp}")
        if resp is None:
            return generate_response(404, body={"error": "Group list not found"})

        group_list_model = GroupListModel(**resp)

        next_item_index = get_next_item_index(group_list_model)

        if next_item_index == None:
            return generate_response(200, body={
                "status": "finished",
                "message": "All items already retrieved"
            })

        current_time = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())
        group_list_repository.update_list_item(group_list_id=group_list_id,
                                               update_idx=next_item_index,
                                               participant_id=participant_id,
                                               retrieved_at=current_time)

        resp = {
            "group_list_id": group_list_id,
            "group_list_item": group_list_model.group_list_items[next_item_index].dict(),
            "participant_id": participant_id,
            "group_list_item_index": next_item_index,
            "retrieved_at": current_time
        }
        return generate_response(200, body=resp)

    except Exception as e:
        return generate_response(500, body="Error inserting data {}".format(str(e)))
