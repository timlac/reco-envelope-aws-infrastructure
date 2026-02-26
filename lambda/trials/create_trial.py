import json
import os
from utils import generate_response, generate_id
from trials.trial_repository import TrialRepository
from trials.models import TrialModel, TrialItemModel


def handler(event, context):
    try:
        data = json.loads(event.get("body") or "[]")
        if not isinstance(data, list):
            return generate_response(400, body="Body must be a JSON array.")
    except Exception:
        return generate_response(400, body="Invalid JSON body.")

    trial_items = []

    for item in data:
        item_model = TrialItemModel(retrieved=0, data=item)
        trial_items.append(item_model)

    trial_id = generate_id()

    model = TrialModel(trial_id=trial_id,
                       trial_items=trial_items)

    if len(model.trial_items) > 1000:
        return generate_response(400, body="Too many trial items, max is 1000")

    try:
        trial_repository = TrialRepository(os.environ["DYNAMODB_TABLE_NAME"])
        resp = trial_repository.create_trial(model, enforce_cap=True)

        return generate_response(200, body=resp)
    except Exception as e:
        return generate_response(500, body="Error inserting data {}".format(str(e)))
