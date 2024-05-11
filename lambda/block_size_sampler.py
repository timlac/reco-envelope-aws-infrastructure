import random


class BlockSizeSampler:

    def __init__(self, block_size_list, list_length):
        self.block_size_list = block_size_list
        self.list_length = list_length
        self.remaining_list_length = list_length
        self.size2num = {}

    def run(self):
        self.generate_initial_samples()
        self.generate_remaining_samples()
        return self.size2num

    def generate_initial_samples(self):
        # Randomly select the number of blocks of each size to sum up to total_rows
        for block_size in self.block_size_list:
            if self.remaining_list_length >= block_size:
                # Ensures we don't exceed total_rows
                max_num_blocks = self.remaining_list_length // block_size
                num_blocks = random.randint(0, max_num_blocks)
                self.size2num[block_size] = num_blocks
                self.remaining_list_length -= num_blocks * block_size
            else:
                self.size2num[block_size] = 0

    def generate_remaining_samples(self):
        while self.remaining_list_length != 0:
            sampled_block_size = random.choice(self.block_size_list)
            if self.remaining_list_length >= sampled_block_size:
                self.size2num[sampled_block_size] += 1
                self.remaining_list_length -= sampled_block_size

