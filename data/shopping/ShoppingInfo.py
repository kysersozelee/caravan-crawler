#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class ShoppingInfo:
    code: str
    title: str
    full_title: str
    data_list: list
