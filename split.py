import os
from random import shuffle
from shutil import copy
import config


def create_data(file_paths, output_dir):
    for filepath in file_paths:
        copy(filepath, output_dir)
    print("{} files copied at {}".format(len(file_paths), output_dir))


split_factor = 0.8
all_files = [os.path.join(config.data_dir, filename) for filename in os.listdir(config.data_dir) if filename.endswith(".json")]
shuffle(all_files)
split = int(len(all_files) * split_factor)
train_files = all_files[:split]
test_files = all_files[split:]
create_data(train_files, config.train_dir)
create_data(test_files, config.test_dir)
