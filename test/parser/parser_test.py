#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

# TODO : test data 읽어 올 때 상대경로 제거
from data.rank.keyword_rank.KeywordRank import KeywordRank
from data.shopping.ShoppingReponse import ShoppingResponse
from data.shopping.age_rate.AgeRateInfo import AgeRateInfo
from data.shopping.click_trend.ClickTrendInfo import ClickTrendInfo
from data.shopping.device_rate.DeviceRateInfo import DeviceRateInfo
from data.shopping.gender_rate.GenderRateInfo import GenderRateInfo
from parser.Parser import Parser


def test_response_data_class():
    with open("%s/../resources/age_rate_sample.txt" % os.path.dirname(os.path.abspath(__file__))) as f:
        response = ShoppingResponse.parse(json.loads(f.readlines()[0]))
        assert response.chart_type == "barChart"
        assert response.code == ""
        assert response.message == ""
        assert response.range == "2017.08.01. ~ 2019.02.01."
        assert response.success is True

        shopping_param = response.shopping_param
        assert shopping_param.age == "10,20,30,40,50,60"
        assert shopping_param.cid == "50001768"
        assert shopping_param.count == 0
        assert shopping_param.date is None
        assert shopping_param.dateRange == "2017.08.01. ~ 2019.02.01."
        assert shopping_param.device == "pc,mo"
        assert shopping_param.end_date == "2019-02-01"
        assert shopping_param.gender == "f,m"
        assert shopping_param.keyword is None
        assert shopping_param.page == 0
        assert shopping_param.start_date == "2017-08-01"
        assert shopping_param.time_unit == "date"
        assert shopping_param.type is None


def test_age_rate_parsing(mocker):
    with open("%s/../resources/age_rate_sample.txt" % os.path.dirname(os.path.abspath(__file__))) as f:
        mocker.patch.object(Parser, "datalab_api_call")
        Parser.datalab_api_call.return_value = json.loads(f.readlines()[0])
        params = Parser.get_params("50001768", "2019-02-01")
        age_rate_info_list = Parser.get_age_rate_info_list(params)

        assert len(age_rate_info_list) == 1
        age_rate_info: AgeRateInfo = age_rate_info_list[0]

        age_rate_list: list = age_rate_info.age_rate_list
        assert len(age_rate_list) == 6
        assert age_rate_list[0].code == "10"
        assert age_rate_list[0].label == "10대"
        assert age_rate_list[0].ratio == 1.83823

        assert age_rate_list[len(age_rate_list) - 1].code == "60"
        assert age_rate_list[len(age_rate_list) - 1].label == "60대"
        assert age_rate_list[len(age_rate_list) - 1].ratio == 8.61796

        assert age_rate_info.code is None
        assert age_rate_info.full_title is None
        assert age_rate_info.title == "50001768"


def test_click_trend_parsing(mocker):
    with open("%s/../resources/click_trend_sample.txt" % os.path.dirname(os.path.abspath(__file__))) as f:
        mocker.patch.object(Parser, "datalab_api_call")
        Parser.datalab_api_call.return_value = json.loads(f.readlines()[0])
        params = Parser.get_params("50001768", "2019-02-01")
        click_trend_info_list = Parser.get_click_trend_info_list(params)

        assert len(click_trend_info_list) == 1
        click_trend_info: ClickTrendInfo = click_trend_info_list[0]

        click_trend_list: list = click_trend_info.click_trend_list
        assert len(click_trend_list) == 549
        assert click_trend_list[0].period == "20170801"
        assert click_trend_list[0].value == 22.82894

        assert click_trend_list[len(click_trend_list) - 1].period == "20190131"
        assert click_trend_list[len(click_trend_list) - 1].value == 21.27836

        assert click_trend_info.code == "50001768"
        assert click_trend_info.full_title == "스포츠/레저 > 등산 > 등산화"
        assert click_trend_info.title == "등산화"


def test_device_rate_parsing(mocker):
    with open("%s/../resources/device_rate_sample.txt" % os.path.dirname(os.path.abspath(__file__))) as f:
        mocker.patch.object(Parser, "datalab_api_call")
        Parser.datalab_api_call.return_value = json.loads(f.readlines()[0])
        params = Parser.get_params("50001768", "2019-02-01")
        device_rate_info_list = Parser.get_device_rate(params)

        assert len(device_rate_info_list) == 1
        device_rate_info: DeviceRateInfo = device_rate_info_list[0]

        device_rate_info_list: list = device_rate_info.device_rate_list
        assert len(device_rate_info_list) == 2
        assert device_rate_info_list[0].code == "mo"
        assert device_rate_info_list[0].label == "모바일"
        assert device_rate_info_list[0].ratio == 100.0

        assert device_rate_info_list[len(device_rate_info_list) - 1].code == "pc"
        assert device_rate_info_list[len(device_rate_info_list) - 1].label == "PC"
        assert device_rate_info_list[len(device_rate_info_list) - 1].ratio == 14.39998

        assert device_rate_info.code is None
        assert device_rate_info.full_title is None
        assert device_rate_info.title == "50001768"


def test_gender_rate_parsing(mocker):
    with open("%s/../resources/gender_rate_sample.txt" % os.path.dirname(os.path.abspath(__file__))) as f:
        mocker.patch.object(Parser, "datalab_api_call")
        Parser.datalab_api_call.return_value = json.loads(f.readlines()[0])
        params = Parser.get_params("50001768", "2019-02-01")
        gender_rate_info_list = Parser.get_gender_rate(params)

        assert len(gender_rate_info_list) == 1
        gender_rate_info: GenderRateInfo = gender_rate_info_list[0]

        gender_rate_list: list = gender_rate_info.gender_rate_list
        assert len(gender_rate_list) == 2
        assert gender_rate_list[0].code == "f"
        assert gender_rate_list[0].label == "여성"
        assert gender_rate_list[0].ratio == 59.05537

        assert gender_rate_list[len(gender_rate_list) - 1].code == "m"
        assert gender_rate_list[len(gender_rate_list) - 1].label == "남성"
        assert gender_rate_list[len(gender_rate_list) - 1].ratio == 100.0

        assert gender_rate_info.code is None
        assert gender_rate_info.full_title is None
        assert gender_rate_info.title == "50001768"

        assert True


def test_keyword_rank_parsing(mocker):
    with open("%s/../resources/keyword_rank_sample.txt" % os.path.dirname(os.path.abspath(__file__))) as f:
        mocker.patch.object(Parser, "datalab_api_call")
        Parser.datalab_api_call.return_value = json.loads(f.readlines()[0])
        params = Parser.get_params("50001768", "2019-02-01")
        keyword_rank_list = Parser.get_keyword_rank(params)

        assert len(keyword_rank_list) == 20
        keyword_rank: KeywordRank = keyword_rank_list[0]
        assert keyword_rank.keyword == "등산화"
        assert keyword_rank.linkId == "등산화"
