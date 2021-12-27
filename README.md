### Steps to get training and test data
1. Download the `scorecards.zip` datapack and unzip it. This will create a directory called `scorecards`.
2. Create two directories: `train` and `test`
3. Run `split.py`. This essentially splits the `scorecards` data into two and places the files in `train` and `test` directories.
4. Run `train.py` to run training via GBDT.