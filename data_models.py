from dataclasses import dataclass
from utils import *


@dataclass(frozen=False)
class BattingFeatures:
    runs: int
    balls_faced: int
    bat_pos: int
    inn_num: int

    def __init__(self, batting_dict: dict, bat_pos: int, inn_num: int):
        self.runs = str2int(batting_dict.get("R", "0"))
        self.balls_faced = str2int(batting_dict.get("B", "0"))
        self.bat_pos = bat_pos
        self.inn_num = inn_num


@dataclass(frozen=False)
class BowlingFeatures:
    wickets: int
    runs_given: int
    overs: float
    inn_num: int

    def __init__(self, bowling_dict: dict, inn_num: int):
        self.wickets = str2int(bowling_dict.get("W", "0"))
        self.runs_given = str2int(bowling_dict.get("R", "0"))
        self.overs = str2float(bowling_dict.get("O", "0"))
        self.inn_num = inn_num


@dataclass(frozen=False)
class PerformanceFeatures:
    bat_inn_num: int
    bowl_inn_num: int
    runs: int = 0
    balls_faced: int = 0
    bat_pos: int = 0
    wickets: int = 0
    runs_given: int = 0
    overs_bowled: float = 0.0

    def add_batting(self):