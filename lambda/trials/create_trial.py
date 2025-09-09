import json
import os
from utils import generate_response, generate_id
from trials.trial_repository import TrialRepository
from trials.models import TrialModel, TrialItemModel


def handler(event, context):
    data = json.loads(event["body"])

    trial_items = []

    for item in data:
        item_model = TrialItemModel(retrieved=0, data=item)
        trial_items.append(item_model)

    trial_id = generate_id()

    model = TrialModel(trial_id=trial_id,
                       trial_items=trial_items)

    print("logging model:")
    print(model)

    try:
        trial_repository = TrialRepository(os.environ["DYNAMODB_TABLE_NAME"])
        resp = trial_repository.create_trial(model)

        return generate_response(200, body=resp)
    except Exception as e:
        return generate_response(500, body="Error inserting data {}".format(str(e)))
