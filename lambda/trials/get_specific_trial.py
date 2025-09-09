import os
from utils import generate_response
from trials.trial_repository import TrialRepository
from trials.models import TrialModel

def handler(event, context):

    trial_id = event['pathParameters']['trial_id']
    query_params = event['queryStringParameters']

    # handle the fact that event['queryStringParameters'] evaluates to None if there are no query parameters
    if query_params:
        only_retrieved_str = query_params.get("only_retrieved", 0)
        only_retrieved = only_retrieved_str == '1'
    else:
        only_retrieved = False

    print(f"only_retrieved: {only_retrieved}")
    print(f"trial_id: {trial_id}")

    try:
        trial_repository = TrialRepository(os.environ["DYNAMODB_TABLE_NAME"])
        resp = trial_repository.get_trial(trial_id)

        if not resp:
            return generate_response(404, "Trial id not found")

        model = TrialModel(**resp)

        if only_retrieved:
            model.trial_items = [item for item in model.trial_items if item.retrieved == 1]

        return generate_response(200, body=model.dict())
    except Exception as e:
        return generate_response(500, body="Error inserting data {}".format(str(e)))
