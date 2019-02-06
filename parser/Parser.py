#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import random
import ssl
import urllib.request
from time import sleep
from typing import Optional
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from data.category.Category import Category
from data.rank.RankReponse import RankResponse
from data.rank.keyword_rank.KeywordRank import KeywordRank
from data.shopping.ShoppingInfo import ShoppingInfo
from data.shopping.ShoppingParam import ShoppingParam
from data.shopping.ShoppingReponse import ShoppingResponse
from data.shopping.age_rate.AgeRate import AgeRate
from data.shopping.click_trend.ClickTrend import ClickTrend
from data.shopping.device_rate.DeviceRate import DeviceRate
from data.shopping.gender_rate.GenderRate import GenderRate
from db.DbConnector import DbConnector


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
    CATEGORY_KEYWORD_RANK = "getCategoryKeywordRank"
    CATEGORY_AGE_RATE = "getCategoryAgeRate"
    CATEGORY_GENDER_RATE = "getCategoryGenderRate"
    CATEGORY_DEVICE_RATE = "getCategoryDeviceRate"
    CATEGORY_CLICK_TREND = "getCategoryClickTrend"
    CATEGORY = "getCategory"

    SHOPPING_INSIGHT_URL = "https://datalab.naver.com/shoppingInsight"

    _instance = None
    _inited = False

    _ua = UserAgent()
    _proxies = []

    def __new__(cls):
        if Parser._instance is None:
            Parser._instance = super().__new__(cls)
        elif not isinstance(Parser._instance, cls):
            raise TypeError
        return Parser._instance

    def __init__(self):
        super().__init__()
        ssl._create_default_https_context = ssl._create_unverified_context
        self.init_proxy()
        logging.getLogger().setLevel(logging.INFO)

        self._inited = True

    def init_proxy(self):
        proxies_req = urllib.request.Request('https://www.sslproxies.org/')
        proxies_req.add_header('User-Agent', self._ua.random)
        proxies_doc = urllib.request.urlopen(proxies_req).read().decode('utf8')
        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')
        for row in proxies_table.tbody.find_all('tr'):
            self._proxies.append({
                'ip': row.find_all('td')[0].string,
                'port': row.find_all('td')[1].string
            })

    @classmethod
    def get_random_proxy(cls):
        proxy_index = cls.random_proxy()
        return cls._proxies[proxy_index]

    @classmethod
    def random_proxy(cls):
        return random.randint(0, len(cls._proxies) - 1)

    @classmethod
    def get_url(cls, key: str):
            return "{0}/{1}.naver".format(cls.SHOPPING_INSIGHT_URL, key)

    @classmethod
    def shopping_request(cls, key: str, params: dict, use_random_proxy=False) -> (ShoppingParam, list):
        url = cls.get_url(key)

        response: Optional[dict] = cls.datalab_api_call(url, params, use_random_proxy=use_random_proxy)
        if response is None:
            logging.error("Got Empty Response! url:{}, params:{}".format(url, params))
            return None, []

        shopping_response = ShoppingResponse.parse(response)

        info_list = []
        for result in shopping_response.results:
            code = result["code"]
            title = result["title"]
            full_title = result["fullTitle"]
            data = result["data"]
            if key == cls.CATEGORY_AGE_RATE:
                data_list: list = AgeRate.parse(data)
                info_list.append(ShoppingInfo(code, title, full_title, data_list))
            elif key == cls.CATEGORY_GENDER_RATE:
                data_list: list = GenderRate.parse(data)
                info_list.append(ShoppingInfo(code, title, full_title, data_list))
            elif key == cls.CATEGORY_DEVICE_RATE:
                data_list: list = DeviceRate.parse(data)
                info_list.append(ShoppingInfo(code, title, full_title, data_list))
            elif key == cls.CATEGORY_CLICK_TREND:
                data_list: list = ClickTrend.parse(data)
                info_list.append(ShoppingInfo(code, title, full_title, data_list))

        return shopping_response.shopping_param, info_list

    @classmethod
    def get_keyword_rank(cls, params: dict, use_random_proxy=False) -> (str, list):
        url = cls.get_url(cls.CATEGORY_KEYWORD_RANK)
        response = cls.datalab_api_call(url, params, use_random_proxy=use_random_proxy)
        if response is None:
            logging.error("Got Empty Response! url:{} params:{}".format(url, params))
            return None, []

        rank_response = RankResponse.parse(response)

        return rank_response.range, KeywordRank.parse(rank_response)

    @classmethod
    def datalab_api_call(cls,
                         url: str,
                         params: dict,
                         path_params: str = None,
                         use_random_proxy=False) -> Optional[dict]:
        request_url = url if path_params is None else "{0}?{1}".format(url, path_params)
        data = urlencode(params).encode("utf-8")

        req = urllib.request.Request(request_url)
        req.add_header("Origin", "https://datalab.naver.com")
        req.add_header('User-Agent', cls._ua.random)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("referer", "https://datalab.naver.com/shoppingInsight/sCategory.naver")

        for i in range(1, 3):

            if use_random_proxy:
                proxy = cls.get_random_proxy()
                authinfo = urllib.request.HTTPSHandler()
                proxy_support = urllib.request.ProxyHandler({"https": proxy['ip'] + ':' + proxy['port']})

                opener = urllib.request.build_opener(proxy_support, authinfo, urllib.request.CacheFTPHandler)
                urllib.request.install_opener(opener)

            try:
                with urllib.request.urlopen(req, timeout=5, data=data) as response:
                    response_code = response.getcode()

                    if response_code is 200:
                        response_body = response.read()
                        response_body_dict = json.loads(response_body.decode("utf-8"))
                        logging.info(response_body_dict)
                        response.close()

                        return response_body_dict
                    else:
                        logging.error("Error to Request. response_code:{}" % response)
            except Exception as e:
                logging.error("Error to Request. %s" % 'e')
        return None

    @classmethod
    def insert_all_categories(cls, cid=0, wait_sec=1):
        category = cls.get_category(cid=cid, use_random_proxy=True)
        DbConnector().insert_category(category)

        for child_category in category.child_list:
            if child_category.leaf:
                DbConnector().insert_category(child_category)
            else:
                cls.insert_all_categories(child_category.cid)

    @classmethod
    def get_category(cls, cid=0, use_random_proxy=False):
        response = cls.datalab_api_call(url=cls.get_url(cls.CATEGORY),
                                        params={},
                                        path_params="cid=%d" % cid,
                                        use_random_proxy=use_random_proxy
                                        )
        if response is not None:
            return Category.parse(response)
        else:
            return None

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
