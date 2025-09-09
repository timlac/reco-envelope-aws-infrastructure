import os
import datetime
from zoneinfo import ZoneInfo
import json
from utils import generate_response
from trials.trial_repository import TrialRepository
from trials.models import TrialModel, TrialItemModel


def get_next_item_index(trial_model):
    next_item_index = None
    for index, item in enumerate(trial_model.trial_items):
        if item.retrieved == 0:
            next_item_index = index
            break
        elif item.retrieved == 1:
            continue
        else:
            raise ValueError(f"Something went wrong, retrieved attribute is not 1, or 0, it is: {item.retrieved}")
    return next_item_index


def handler(event, context):
    trial_id = event['pathParameters']['trial_id']

    body = json.loads(event['body'])
    participant_id = body['participant_id']
    administrator_id = body['administrator']

    print(f"trial_id: {trial_id}")
    print(f"participant_id: {participant_id}")
    print(f"administrator_id: {administrator_id}")

    try:
        trial_repository = TrialRepository(os.environ["DYNAMODB_TABLE_NAME"])
        resp = trial_repository.get_trial(trial_id)

        print(f"resp: {resp}")
        if resp is None:
            return generate_response(404, body={"error": "Trial id not found"})

        trial_model = TrialModel(**resp)
        next_item_index = get_next_item_index(trial_model)

        if next_item_index == None:
            return generate_response(200, body={
                "status": "finished",
                "message": "All items already retrieved"
            })

        current_time = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())
        trial_repository.update_list_item(trial_id=trial_id,
                                          update_idx=next_item_index,
                                          participant_id=participant_id,
                                          retrieved_at=current_time,
                                          administrator_id=administrator_id)

        resp = {
            "trial_id": trial_id,
            "trial_items": trial_model.trial_items[next_item_index].model_dump(),
            "participant_id": participant_id,
            "trial_item_index": next_item_index,
            "retrieved_at": current_time
        }
        return generate_response(200, body=resp)

    except ValueError as e:
        return generate_response(400, body={"error": str(e)})
    except Exception as e:
        return generate_response(500, body="Error inserting data {}".format(str(e)))
