#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import ssl
import urllib.request
from time import sleep
from typing import Optional
from urllib.parse import urlencode

from data.category.Category import Category
from data.rank.RankReponse import RankResponse
from data.rank.keyword_rank.KeywordRank import KeywordRank
from data.shopping.ShoppingReponse import ShoppingResponse
from data.shopping.age_rate.AgeRate import AgeRate
from data.shopping.age_rate.AgeRateInfo import AgeRateInfo
from data.shopping.click_trend.ClickTrend import ClickTrend
from data.shopping.click_trend.ClickTrendInfo import ClickTrendInfo
from data.shopping.device_rate.DeviceRate import DeviceRate
from data.shopping.device_rate.DeviceRateInfo import DeviceRateInfo
from data.shopping.gender_rate.GenderRate import GenderRate
from data.shopping.gender_rate.GenderRateInfo import GenderRateInfo


class ParserMeta(type):
    def __new__(mcs, name, bases, attrs):
        if "__init__" in attrs:
            ctor = attrs["__init__"]

            def init(cls):
                if not cls._inited:
                    ctor(cls)

            attrs["__init__"] = init
        return super().__new__(mcs, name, bases, attrs)


class Parser(metaclass=ParserMeta):
    CATEGORY_KEYWORD_RANK = "get_category_keyword_rank"
    CATEGORY_AGE_RATE = "get_category_age_rate"
    CATEGORY_GENDER_RATE = "get_category_gender_rate"
    CATEGORY_DEVICE_RATE = "get_category_device_rate"
    CATEGORY_CLICK_TREND = "get_category_click_trend"

    URLS = {CATEGORY_CLICK_TREND: "https://datalab.naver.com/shoppingInsight/getCategoryClickTrend.naver",
            CATEGORY_DEVICE_RATE: "https://datalab.naver.com/shoppingInsight/getCategoryDeviceRate.naver",
            CATEGORY_GENDER_RATE: "https://datalab.naver.com/shoppingInsight/getCategoryGenderRate.naver",
            CATEGORY_AGE_RATE: "https://datalab.naver.com/shoppingInsight/getCategoryAgeRate.naver",
            CATEGORY_KEYWORD_RANK: "https://datalab.naver.com/shoppingInsight/getCategoryKeywordRank.naver"
            }

    _instance = None
    _inited = False

    def __new__(cls):
        if Parser._instance is None:
            Parser._instance = super().__new__(cls)
        elif not isinstance(Parser._instance, cls):
            raise TypeError
        return Parser._instance

    def __init__(self):
        super().__init__()
        ssl._create_default_https_context = ssl._create_unverified_context
        logging.getLogger().setLevel(logging.INFO)

        self._inited = True

    @classmethod
    def get_url(cls, key: str):
        return cls.URLS.get(key)

    @classmethod
    def get_age_rate_info_list(cls, params: dict) -> list:
        url = cls.get_url(cls.CATEGORY_AGE_RATE)
        response: Optional[dict] = cls.datalab_api_call(url, params)
        if response is None:
            logging.error("Got Empty Response! url:{} params:{}".format(url, params))
            return []

        shopping_response = ShoppingResponse.parse(response)

        age_rate_info_list = []
        for result in shopping_response.results:
            code = result["code"]
            title = result["title"]
            full_title = result["fullTitle"]
            age_rate_list: list = AgeRate.parse(result["data"])

            age_rate_info_list.append(AgeRateInfo(code, title, full_title, age_rate_list))

        return age_rate_info_list

    @classmethod
    def get_click_trend_info_list(cls, params: dict) -> list:
        url = cls.get_url(cls.CATEGORY_CLICK_TREND)
        response: Optional[dict] = cls.datalab_api_call(url, params)
        if response is None:
            logging.error("Got Empty Response! url:{} params:{}".format(url, params))
            return []

        shopping_response = ShoppingResponse.parse(response)

        click_trend_info_list = []
        for result in shopping_response.results:
            code = result["code"]
            title = result["title"]
            full_title = result["fullTitle"]
            click_trend_list: list = ClickTrend.parse(result["data"])

            click_trend_info_list.append(ClickTrendInfo(code, title, full_title, click_trend_list))

        return click_trend_info_list

    @classmethod
    def get_device_rate(cls, params: dict) -> list:
        url = cls.get_url(cls.CATEGORY_DEVICE_RATE)
        response: Optional[dict] = cls.datalab_api_call(url, params)
        if response is None:
            logging.error("Got Empty Response! url:{} params:{}".format(url, params))
            return []

        shopping_response = ShoppingResponse.parse(response)

        device_rate_info_list = []
        for result in shopping_response.results:
            code = result["code"]
            title = result["title"]
            full_title = result["fullTitle"]
            device_rate_list: list = DeviceRate.parse(result["data"])

            device_rate_info_list.append(DeviceRateInfo(code, title, full_title, device_rate_list))

        return device_rate_info_list

    @classmethod
    def get_gender_rate(cls, params: dict) -> list:
        url = cls.get_url(cls.CATEGORY_GENDER_RATE)
        response: Optional[dict] = cls.datalab_api_call(url, params)
        if response is None:
            logging.error("Got Empty Response! url:{} params:{}".format(url, params))
            return []

        shopping_response = ShoppingResponse.parse(response)

        gender_rate_info_list = []
        for result in shopping_response.results:
            code = result["code"]
            title = result["title"]
            full_title = result["fullTitle"]
            gender_rate_list: list = GenderRate.parse(result["data"])

            gender_rate_info_list.append(GenderRateInfo(code, title, full_title, gender_rate_list))

        return gender_rate_info_list

    @classmethod
    def get_keyword_rank(cls, params: dict) -> list:
        url = cls.get_url(cls.CATEGORY_KEYWORD_RANK)
        response = cls.datalab_api_call(url, params)
        if response is None:
            logging.error("Got Empty Response! url:{} params:{}".format(url, params))
            return []

        rank_response = RankResponse.parse(response)

        return KeywordRank.parse(rank_response)

    @classmethod
    def datalab_api_call(cls, url: str, params: dict, path_params: str = None) -> Optional[dict]:
        request_url = url if path_params is None else "{0}?{1}".format(url, path_params)
        data = urlencode(params).encode("utf-8")

        req = urllib.request.Request(request_url)
        req.add_header("Origin", "https://datalab.naver.com")
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("referer", "https://datalab.naver.com/shoppingInsight/sCategory.naver")

        try:
            with urllib.request.urlopen(req, data=data) as response:
                response_code = response.getcode()

                if response_code is 200:
                    response_body = response.read()
                    response_body_dict = json.loads(response_body.decode("utf-8"))
                    logging.info(response_body_dict)
                    response.close()

                    return response_body_dict
                else:
                    logging.error("Error to Request. response_code:{}" % response)
                    return None
        except Exception as e:
            logging.error("Error to Open URL for Request. error:{}" % e.message)
            return None

    # Warning: 2019/02/01 기준 카테고리가 4,485개 존재. 50,000,000 ~ 50,004,485
    # 아래 메소드는 모든 카테고리를 재귀를 돌며 데이터 크롤링하는 함수로 시간이 매우 많이 걸림. sleep 없이 사용하면 접근 거부됨.
    @classmethod
    def get_all_categories(cls, url="https://datalab.naver.com/shoppingInsight/getCategory.naver", cid=0):
        response = cls.datalab_api_call(url=url,
                                        params={},
                                        path_params="cid=%d" % cid
                                        )
        categories = Category.parse(response)

        for child_category in categories.child_list:
            child_cid = child_category.cid
            full_path = child_category.full_path
            logging.info(full_path)
            sleep(3)
            if child_category.leaf:
                return [child_category]
            grand_child_category_list = cls.get_all_categories(cid=child_cid)
            child_category.child_list.append(grand_child_category_list)

        return categories

    @classmethod
    def get_category(cls, url="https://datalab.naver.com/shoppingInsight/getCategory.naver", cid=0):
        response = cls.datalab_api_call(url=url,
                                        params={},
                                        path_params="cid=%d" % cid
                                        )
        return Category.parse(response)

    @classmethod
    def get_params(cls, cid: str, end_date: str, start_date: str = "2017-08-01") -> dict:
        return {"cid": cid,
                "timeUnit": "date",
                "startDate": start_date,
                "endDate": end_date,
                "device": "pc,mo",
                "gender": "f,m",
                "age": "10,20,30,40,50,60",
                }
