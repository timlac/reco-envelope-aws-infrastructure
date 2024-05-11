import numpy as np
import random


def generate_blocks(block_size_list, list_length, treatment_groups):
    ret = []
    remaining_list_length = list_length

    block_index = 0
    while remaining_list_length > 0:
        sampled_block_size = random.choice(block_size_list)
        if sampled_block_size <= remaining_list_length:
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
