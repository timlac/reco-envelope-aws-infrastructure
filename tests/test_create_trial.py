import json
import os
from dotenv import load_dotenv

from list_generation.generate_randomization_list import handler as generate_randomization_list_handler

from trials.create_trial import handler as create_trial

load_dotenv()

TABLE_NAME = os.getenv("ENVELOPE_TABLE_DEV")
os.environ["DYNAMODB_TABLE_NAME"] = TABLE_NAME
os.environ['AWS_PROFILE'] = 'personalAcc'


body = {
    "block_size_list": [
        "12",
        "24"
    ],
    "list_length": "240",
    "treatment_groups": {
        "C": "2",
        "B": "5",
        "A": "6"
    }
}


print(len(body["treatment_groups"]))


# Convert the body dictionary to a JSON string
json_body = json.dumps(body)

# Create an event dictionary with the body as a JSON string
event = {
    "body": json_body
}


ret = generate_randomization_list_handler(event=event, context=None)

body = json.loads(ret["body"])
print(body)

event = {
    "body": json.dumps(body)
}

ret = create_trial(event=event, context=None)

print(ret)