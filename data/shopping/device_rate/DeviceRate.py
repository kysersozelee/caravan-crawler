from dataclasses import dataclass#!/usr/bin/env python
# -*- coding: utf-8 -*-




@dataclass(frozen=True)
class DeviceRate:
    code: str
    label: str
    ratio: float

    @staticmethod
    def parse(data_list: list) -> list:
        return list(map(lambda data: DeviceRate(data['code'], data['label'], data['ratio']), data_list))
