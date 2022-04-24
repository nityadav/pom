from dataclasses import dataclass
import utils


@dataclass(frozen=False)
class BattingFeatures:
    runs: int
    balls_faced: int
    bat_pos: int
    inn_num: int

    def __init__(self, batting_dict: dict, bat_pos: int, inn_num: int):
        self.runs = utils.str2int(batting_dict.get("R", "0"))
        self.balls_faced = utils.str2int(batting_dict.get("B", "0"))
        self.bat_pos = bat_pos
        self.inn_num = inn_num


@dataclass(frozen=False)
class BowlingFeatures:
    wickets: int
    runs_given: int
    overs: float
    inn_num: int

    def __init__(self, bowling_dict: dict, inn_num: int):
        self.wickets = utils.str2int(bowling_dict.get("W", "0"))
        self.runs_given = utils.str2int(bowling_dict.get("R", "0"))
        self.overs = utils.str2float(bowling_dict.get("O", "0"))
        self.inn_num = inn_num


@dataclass(frozen=False)
class PerformanceFeatures:
    bat_inn_num: int = 0
    bowl_inn_num: int = 0
    runs: int = 0
    balls_faced: int = 0
    bat_pos: int = 0
    wickets: int = 0
    runs_given: int = 0
    overs_bowled: float = 0.0

    def add_batting(self, btf: BattingFeatures):
        self.runs = btf.runs
        self.balls_faced = btf.balls_faced
        self.bat_pos = btf.bat_pos
        self.bat_inn_num = btf.inn_num

    def add_bowling(self, bwf: BowlingFeatures):
        self.wickets = bwf.wickets
        self.runs_given = bwf.runs_given
        self.overs_bowled = bwf.overs
        self.bowl_inn_num = bwf.inn_num


@dataclass(frozen=False)
class InningFeatures:
    runs: int = 0
    balls_faced: int = 0
    num_batsmen: int = 0
    wickets: int = 0
    num_bowlers: int = 0
