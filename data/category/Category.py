#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    cid: int
    pid: int
    name: str
    parent_path: str
    level: int
    exps_order: int
    parents: list
    child_list: list
    leaf: bool
    deleted: bool
    svc_use: bool
    sblog_use: bool
    full_path: str

    @staticmethod
    def parse(response: dict):
        child_list = Category.parse_child_list(response['childList'])

        return Category(response['cid'],
                        response['pid'],
                        response['name'],
                        response['parentPath'],
                        response['level'],
                        response['expsOrder'],
                        response['parents'],
                        child_list,
                        response['leaf'],
                        response['deleted'],
                        response['svcUse'],
                        response['sblogUse'],
                        response['fullPath']
                        )

    @staticmethod
    def parse_child_list(child_list: dict) -> list:
        grand_child_list = []
        for child in child_list:
            grand_child_list.append(Category.parse(child))

        return grand_child_list
