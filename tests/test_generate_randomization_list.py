import json
import pandas as pd
from generate_randomization_list import handler

body = {
    "block_size_list": [
        "12",
        "24"
    ],
    "list_length": "240",
    "A": "5",
    "B": "5",
    "C": "2",
    "treatment_groups": {
        "C": "2",
        "B": "5",
        "A": "5"
    }
}

# Convert the body dictionary to a JSON string
json_body = json.dumps(body)

# Create an event dictionary with the body as a JSON string
event = {
    "body": json_body
}


ret = handler(event=event, context=None)

body = json.loads(ret["body"])
print(body)

df = pd.DataFrame(body)

print(df["block_index"].value_counts())