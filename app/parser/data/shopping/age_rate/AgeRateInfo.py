from dataclasses import dataclass


@dataclass(frozen=True)
class AgeRateInfo:
    code: str
    title: str
    full_title: str
    age_rate_list: list
