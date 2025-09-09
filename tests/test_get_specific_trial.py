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
            "trial_id": "2d83d503e8266069362a9aee6ce59db54a9b6bcd50d618adcf3bcafa258dc154"
        },
    "queryStringParameters": {
        "only_retrieved": "0"
    }
}


resp = handler(event, None)

print(resp)