import json
import os
from dotenv import load_dotenv


from get_specific_group_list import handler

load_dotenv()

TABLE_NAME = os.getenv("ENVELOPE_TABLE_DEV")
os.environ["DYNAMODB_TABLE_NAME"] = TABLE_NAME

event = {
    "pathParameters":
        {
            "group_list_id": "5a6ec4955c869e921f32bb4e17edd31827728cc1924c3a21f192c2a068c004cc"
        }
}


resp = handler(event, None)

print(resp)