import os
from random import shuffle
from shutil import copy
import config


def create_data(file_paths, output_dir):
    for filepath in file_paths:
        copy(filepath, output_dir)
    print("{} files copied at {}".format(len(file_paths), output_dir))


if __name__ == '__main__':
    all_files = [os.path.join(config.data_dir, filename) for filename in os.listdir(config.data_dir) if filename.endswith(".json")]
    shuffle(all_files)
    train_split = int(len(all_files) * 0.8)
    dev_split = int(len(all_files) * 0.9)
    train_files = all_files[:train_split]
    dev_files = all_files[train_split:dev_split]
    test_files = all_files[dev_split:]
    create_data(train_files, config.train_dir)
    create_data(dev_files, config.dev_dir)
    create_data(test_files, config.test_dir)
