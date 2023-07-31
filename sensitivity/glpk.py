import re

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


SECOND_ROW = "Marginal   Upper bound          range         range   break point variable"
SEP_ROW = "------ ------------ -- ------------- ------------- -------------  ------------- ------------- ------------- ------------"
END_ROW = "End of report"

ROW_PATTERN = (
    r"^\s*No.\s+Row name\s+St\s+Activity\s+Slack\s+Lower bound\s+Activity\s+Obj coef\s+Obj value at Limiting\s*$"
)
COL_PATTERN = (
    r"^\s*No.\s+Column name\s+St\s+Activity\s+Obj coef\s+Lower bound\s+Activity\s+Obj coef\s+Obj value at Limiting\s*$"
)


class Section(Enum):
    ROW = 1
    COL = 2


@dataclass
class Record:
    no: int
    name: str
    st: str
    activity: float
    slack: Optional[float]
    obj_coef: Optional[float]
    marginal: float
    bounds: Tuple[float, float]
    activity_range: Tuple[float, float]
    obj_coef_range: Tuple[float, float]
    obj_value_break_range: Tuple[float, float]
    limiting_variables: Tuple[Optional[str], Optional[str]]


def float_or_zero(val):
    return float(0) if val == "." else float(val)


def create_record(first_row, second_row, section):
    return Record(
        no=int(first_row[0]),
        name=first_row[1],
        st=first_row[2],
        activity=float_or_zero(first_row[3]),
        slack=float_or_zero(first_row[4]) if section == Section.ROW else None,
        obj_coef=float_or_zero(first_row[4]) if section == Section.COL else None,
        marginal=float_or_zero(second_row[0]),
        bounds=(float_or_zero(first_row[5]), float_or_zero(second_row[1])),
        activity_range=(float_or_zero(first_row[6]), float_or_zero(second_row[2])),
        obj_coef_range=(float_or_zero(first_row[7]), float_or_zero(second_row[3])),
        obj_value_break_range=(float_or_zero(first_row[8]), float_or_zero(second_row[4])),
        limiting_variables=(
            first_row[9] if len(first_row) > 9 else None,
            second_row[5] if len(second_row) > 5 else None,
        ),
    )


def process(filename):
    records = defaultdict(list)
    section = None
    first_row = None

    with open(filename) as f:
        for line in f:
            line = line.strip()

            if (
                line
                and line != SECOND_ROW
                and line != SEP_ROW
                and line != END_ROW
                and not line.startswith("GLPK")
                and not line.startswith("Problem:")
                and not line.startswith("Objective:")
            ):
                if re.match(ROW_PATTERN, line):
                    section = Section.ROW
                elif re.match(COL_PATTERN, line):
                    section = Section.COL
                else:
                    parts = line.split()
                    if len(parts) in (9, 10):  # First row
                        first_row = parts
                    elif len(parts) in (5, 6):  # Second row
                        record = create_record(first_row, parts, section)
                        records[section].append(record)
                    else:
                        raise ValueError(f'Incorrect format for line "{line}"')

    return records
