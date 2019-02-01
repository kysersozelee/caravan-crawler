#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class ClickTrend:
    period: str
    value: float

    @staticmethod
    def parse(data_list: list) -> list:
        return list(map(lambda data: ClickTrend(data['period'], data['value']), data_list))
