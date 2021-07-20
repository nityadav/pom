import json
from data_models import *
from collections import defaultdict


def get_batting_features(batting_dict: dict, bat_pos: int, inn_num: int):
    return BattingFeatures(batting_dict, bat_pos, inn_num)


def get_bowling_features(bowling_dict: dict, inn_num: int):
    return BowlingFeatures(bowling_dict, inn_num)


def get_innings_features(inn_idx, inning):
    inn_num = inn_idx + 1
    battings = {b["BATSMEN"]: get_batting_features(b, b_idx + 1, inn_num) for b_idx, b in enumerate(inning.get("batting", []))}
    bowlings = {b["Bowling"]: get_bowling_features(b, inn_num) for b in inning.get("bowling", [])}
    return battings, bowlings


class Scorecard(object):
    def __init__(self, filepath):
        with open(filepath) as scorecard_f:
            self.scorecard = json.load(scorecard_f)
            all_battings = {}
            all_bowlings = {}
            for inn_idx, inn in enumerate(self.scorecard.get("innings", [])):
                bt, bw = get_innings_features(inn_idx, inn)
                # python 3.5 or greater
                all_battings = {**all_battings, **bt}
                all_bowlings = {**all_bowlings, **bw}
            all_performances = defaultdict(PerformanceFeatures)
            for p, b in all_battings.items():



    def get_match_features(self):


