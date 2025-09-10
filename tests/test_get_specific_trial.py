import os
from dotenv import load_dotenv


from trials.get_specific_trial import handler


os.environ['AWS_PROFILE'] = 'personalAcc'


load_dotenv()

TABLE_NAME = os.getenv("ENVELOPE_TABLE_DEV")
os.environ["DYNAMODB_TABLE_NAME"] = TABLE_NAME

event = {
    "pathParameters":
        {
            "trial_id": "77041e39383b017ad5405cc8ccf2afb93e5d0f0630293104ec22665846dd03ee"
        },
    "queryStringParameters": {
        "only_retrieved": "0"
    }
}


resp = handler(event, None)

print(resp)

trial_item = item['trial_items'][update_idx]