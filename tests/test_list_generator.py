from generate_list import get_items


data = {
    "block_size_list": [
        "12",
        "24"
    ],
    "list_length": "240",
    "A": "6",
    "B": "5",
    "C": "2",
    "treatment_groups": {
        "C": "2",
        "B": "5",
        "A": "6"
    }
}

list_length = int(data["list_length"])
block_size_list = (data["block_size_list"])
block_size_list = [int(x) for x in block_size_list]

treatment_groups = data["treatment_groups"]

print(f"treatment_groups: {treatment_groups}")

treatment_groups_int = {key: int(value) for key, value in treatment_groups.items()}

print(f"Treatment groups int: {treatment_groups_int}")


resp = get_items(treatment_groups_int, 16)

print(resp)

print(len(resp))
