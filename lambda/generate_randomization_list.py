import json
from block_size_sampler import BlockSizeSampler
from generate_list import generate_list
from utils import generate_response


def handler(event, context):
    data = json.loads(event["body"])

    list_length = int(data["list_length"])
    block_size_list = (data["block_size_list"])
    block_size_list = [int(x) for x in block_size_list]

    treatment_groups = data["treatment_groups"]

    print(f"treatment_groups: {treatment_groups}")

    treatment_groups_int = {key: int(value) for key, value in treatment_groups.items()}

    print(f"Treatment groups int: {treatment_groups_int}")

    try:
        sampler = BlockSizeSampler(block_size_list, list_length)
        block_size_dict = sampler.run()

        print(f"Block sizes: {block_size_dict}")

        generated_list = generate_list(block_size_dict, treatment_groups_int)
        return generate_response(200, body=generated_list)
    except Exception as e:
        return generate_response(500, body="Error generating list {}".format(str(e)))









