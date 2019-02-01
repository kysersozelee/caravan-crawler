#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class GenderRateInfo:
    code: str
    title: str
    full_title: str
    gender_rate_list: list
