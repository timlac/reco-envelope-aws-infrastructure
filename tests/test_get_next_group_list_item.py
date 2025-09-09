import json
import os
from dotenv import load_dotenv


os.environ['AWS_PROFILE'] = 'rackspaceAcc'

from trials.get_next_trial_item import handler

load_dotenv()

TABLE_NAME = os.getenv("ENVELOPE_TABLE_DEV")
os.environ["DYNAMODB_TABLE_NAME"] = TABLE_NAME

event = {
    "pathParameters":
        {
            "group_list_id": "caea2310fc38db392849427e06ad89724d556eb2c6996b94e4752b45e9083e8e"
        },
    "body": json.dumps({
        "participant_id": "Tim"
    })
}


resp = handler(event, None)

print(resp)