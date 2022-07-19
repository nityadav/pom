import json
from data_models import *
from collections import defaultdict
import dataclasses


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
            self.pom = self.scorecard.get("pom", None)
            self.performances = defaultdict(PerformanceFeatures)
            all_battings = {}
            all_bowlings = {}
            for inn_idx, inn in enumerate(self.scorecard.get("innings", [])):
                bt, bw = get_innings_features(inn_idx, inn)
                # python 3.5 or greater
                all_battings = {**all_battings, **bt}
                all_bowlings = {**all_bowlings, **bw}
            for p, b in all_battings.items():
                self.performances[p].add_batting(b)
            for p, b in all_bowlings.items():
                self.performances[p].add_bowling(b)
            self.inn1_summary = self._get_innings_summary(1)
            self.inn2_summary = self._get_innings_summary(2)
            self.features_dict = self._get_features_dict()

    def _get_features_dict(self) -> dict:
        inn1_features = {"inn1_{}".format(k): v for k, v in dataclasses.asdict(self.inn1_summary).items()}
        inn2_features = {"inn2_{}".format(k): v for k, v in dataclasses.asdict(self.inn2_summary).items()}
        return {p: {**dataclasses.asdict(bb), **inn1_features, **inn2_features} for p, bb in self.performances.items()}

    def _if_pom(self, player_id) -> int:
        return 1 if self.pom is not None and self.pom == player_id else 0

    def get_features_with_label(self, include_labelled_only=True) -> list:
        features_with_label, player_list = [], []
        for p, f in self.features_dict.items():
            features_with_label.append({**f, "pom": self._if_pom(p)})
            player_list.append(p)
        features_with_label = [{**f, "pom": self._if_pom(p)} for p, f in self.features_dict.items()]
        return [] if include_labelled_only and self.pom is None else features_with_label

    def if_pom_bowler(self):
        if self.pom is not None:
            return 1 if self.performances[self.pom].overs_bowled > 0.0 else 0
        else:
            return None

    def _get_innings_summary(self, inn_num):
        inn_summary = InningFeatures()
        for bb in self.performances.values():
            if bb.bat_inn_num == inn_num:
                if bb.runs is not None:
                    inn_summary.runs += bb.runs
                if bb.balls_faced is not None:
                    inn_summary.balls_faced += bb.balls_faced
                inn_summary.num_batsmen += 1
            if bb.bowl_inn_num == inn_num:
                if bb.wickets is not None:
                    inn_summary.wickets += bb.wickets  # run outs get excluded
                inn_summary.num_bowlers += 1
        return inn_summary


if __name__ == '__main__':
    test_scorecard = Scorecard('scorecards/64180.json')
    with open('test.json', 'w') as test_f:
        json.dump(test_scorecard.get_features_with_label(), test_f)
