import numpy as np
import random


def generate_list(block_size_dict, groups):
    ret = []

    current_block = 1

    for index, (size, number_of_blocks) in enumerate(block_size_dict.items()):
        for block in range(number_of_blocks):
            items = get_items(groups, size)

            items_with_index = []
            for item in items:
                items_with_index.append({"block_index": current_block, "item": item})
            ret.extend(items_with_index)

            current_block += 1
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
