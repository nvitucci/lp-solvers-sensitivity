import csv
import math

from dataclasses import dataclass
from typing import Optional

# Limits from the CBC code (I think from
# https://github.com/coin-or/Cbc/blob/d4272be8c5e3b231f35e7555587e427a5f69d1ed/src/CbcParamUtils.cpp#L1302)
MAX_VAL = 1e100
MIN_VAL = -1e100


@dataclass
class Record:
    ranging: int
    name: str
    increase: float
    inc_variable: Optional[str]
    decrease: float
    dec_variable: Optional[str]


def fix_float(f):
    if f >= MAX_VAL:
        return math.inf
    elif f <= MIN_VAL:
        return -math.inf
    else:
        return f


def convert(d):
    assert d.keys() == {"ranging", "name", "increase", "inc_variable", "decrease", "dec_variable"}

    return Record(
        ranging=int(d["ranging"]),
        name=d["name"],
        increase=fix_float(float(d["increase"])),
        inc_variable=d["inc_variable"] if d["inc_variable"] else None,
        decrease=fix_float(float(d["decrease"])),
        dec_variable=d["dec_variable"] if d["dec_variable"] else None,
    )


def process(filename):
    with open(filename) as f:
        reader = csv.DictReader(
            f, fieldnames=["ranging", "name", "increase", "inc_variable", "decrease", "dec_variable"]
        )
        # Skip first row (header) because the field names are assigned
        next(reader)

        return [convert(el) for el in reader]
