def str2float(s: str) -> float:
    s = s.replace("-", "")
    s = s.replace("*", "")
    return float(s) if s else 0.0


def str2int(s: str) -> int:
    return int(str2float(s))
