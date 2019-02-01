#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class ShoppingParam:
    start_date: str
    end_date: str
    time_unit: str
    cid: str
    device: str
    gender: str
    age: str
    keyword: str
    page: int
    count: int
    type: str
    date: str
    dateRange: str

    @staticmethod
    def parse(shopping_param: dict):
        return ShoppingParam(shopping_param['startDate'],
                             shopping_param['endDate'],
                             shopping_param['timeUnit'],
                             shopping_param['cid'],
                             shopping_param['device'],
                             shopping_param['gender'],
                             shopping_param['age'],
                             shopping_param['keyword'],
                             shopping_param['page'],
                             shopping_param['count'],
                             shopping_param['type'],
                             shopping_param['date'],
                             shopping_param['dateRange']
                             )
