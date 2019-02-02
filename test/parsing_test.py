#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os

logging.getLogger().setLevel(logging.INFO)


def test_age_rate_parsing():
    with open('%s/resources/age_rate_sample.txt' % os.path.dirname(os.path.abspath(__file__))) as f:
        response = json.loads(f.readlines()[0])

        result = response['result'][0]
        assert "title" in result
        assert "fullTitle" in result
        assert "code" in result

        data_list = response['result'][0]['data']
        for data in data_list:
            assert "code" in data
            assert "label" in data
            assert "ratio" in data
            assert data["code"] in ["10", "20", "30", "40", "50", "60"]
            assert data["label"] in ["10대", "20대", "30대", "40대", "50대", "60대"]


def test_click_trend_parsing():
    with open('%s/resources/click_trend_sample.txt' % os.path.dirname(os.path.abspath(__file__))) as f:
        response = json.loads(f.readlines()[0])

        result = response['result'][0]
        assert "title" in result
        assert "fullTitle" in result
        assert "code" in result

        data = response['result'][0]['data']
        assert "period" in data[0]
        assert "value" in data[0]


def test_device_rate_parsing():
    with open('%s/resources/device_rate_sample.txt' % os.path.dirname(os.path.abspath(__file__))) as f:
        response = json.loads(f.readlines()[0])

        result = response['result'][0]
        assert "title" in result
        assert "fullTitle" in result
        assert "code" in result

        data_list = response['result'][0]['data']
        assert len(data_list) == 2

        for data in data_list:
            assert "code" in data
            assert "label" in data
            assert "ratio" in data
            assert data["code"] in ("mo", "pc")
            assert data["label"] in ("모바일", "PC")


def test_gender_rate_parsing():
    with open('%s/resources/gender_rate_sample.txt' % os.path.dirname(os.path.abspath(__file__))) as f:
        response = json.loads(f.readlines()[0])

        result = response['result'][0]
        assert "title" in result
        assert "fullTitle" in result
        assert "code" in result

        data_list = response['result'][0]['data']
        assert len(data_list) == 2

        for data in data_list:
            assert "code" in data
            assert "label" in data
            assert "ratio" in data
            assert data["code"] in ("f", "m")
            assert data["label"] in ("여성", "남성")


def test_keyword_rank_parsing():
    with open('%s/resources/keyword_rank_sample.txt' % os.path.dirname(os.path.abspath(__file__))) as f:
        response = json.loads(f.readlines()[0])

        assert "date" in response
        assert "range" in response
        ranks = response["ranks"]

        for rank in ranks:
            assert "rank" in rank
            assert "keyword" in rank
            assert "linkId" in rank
