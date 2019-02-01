from dataclasses import dataclass


@dataclass(frozen=True)
class ClickTrendInfo:
    code: str
    title: str
    full_title: str
    click_trend_list: list
