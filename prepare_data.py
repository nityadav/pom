import os
from random import shuffle
from shutil import copy
from utils import json_to_svm
import config


def create_data(file_paths, output_dir):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    for filepath in file_paths:
        copy(filepath, output_dir)
    print("{} files copied at {}".format(len(file_paths), output_dir))


if __name__ == '__main__':
    all_files = [os.path.join(config.scorecards_dir, filename) for filename in os.listdir(config.scorecards_dir) if filename.endswith('.json')]
    shuffle(all_files)
    train_split = int(len(all_files) * 0.8)
    dev_split = int(len(all_files) * 0.9)
    train_files = all_files[:train_split]
    dev_files = all_files[train_split:dev_split]
    test_files = all_files[dev_split:]
    if not os.path.isdir(config.data_dir):
        os.mkdir(config.data_dir)
    create_data(train_files, config.train_dir)
    create_data(dev_files, config.dev_dir)
    create_data(test_files, config.test_dir)

    # convert to svm format - one file for each set
    json_to_svm(config.train_dir, config.features_file, config.train_file)
    json_to_svm(config.dev_dir, config.features_file, config.dev_file)
    json_to_svm(config.test_dir, config.features_file, config.test_file)
