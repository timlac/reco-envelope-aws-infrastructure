import numpy as np
import random


def assert_proportions(block_size_list, treatment_groups):
    for block_size in block_size_list:
        assert block_size % len(treatment_groups) == 0


def generate_blocks(block_size_list, list_length, treatment_groups):
    ret = []
    remaining_list_length = list_length

    block_size_list.sort()

    print(block_size_list)

    block_index = 0
    while remaining_list_length > 0:

        if remaining_list_length > block_size_list[0]:
            print(f"\nremaining list length {remaining_list_length}, is larger than block size: {block_size_list[0]}")

            sampled_block_size = random.choice(block_size_list)

            print(f"Sampled block size: {sampled_block_size}")

            if sampled_block_size > remaining_list_length:

                print(f"sampled block size: {sampled_block_size} is larger than remaining list length: {remaining_list_length}")
                print("will continue")
                continue
        else:
            print(f"remaining list length {remaining_list_length} is smaller than block size: {block_size_list[0]}")
            sampled_block_size = block_size_list[0]

        items = get_items(treatment_groups, sampled_block_size)
        items_with_index = []
        for item in items:
            items_with_index.append({"block_index": block_index, "group": item})

        ret.extend(items_with_index)
        block_index += 1
        remaining_list_length -= sampled_block_size

    return ret


def get_items(original_groups, desired_total):
    # Extract the keys and the original weights
    keys = list(original_groups.keys())
    weights = np.array(list(original_groups.values()))

    # Calculate the normalized weights to reach the desired total
    scaled_weights = np.round((weights / weights.sum()) * desired_total).astype(int)
    # Create a new dictionary with the scaled weights
    new_groups = dict(zip(keys, scaled_weights))

    # Create the list of items according to the adjusted weights
    items_list = [key for key, count in new_groups.items() for _ in range(count)]

    random.shuffle(items_list)

    return items_list
