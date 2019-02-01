import json
import logging
import ssl
import urllib
from urllib.parse import urlencode

from main.parser.data.AgeRate import AgeRate
from main.parser.data.ShoppingReponse import ShoppingResponse


class ParserMeta(type):
    def __new__(mcs, name, bases, attrs):
        if '__init__' in attrs:
            ctor = attrs['__init__']

            def init(cls):
                if not cls._inited:
                    ctor(cls)

            attrs['__init__'] = init
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
    def get_age_rate(cls, params: dict) -> list:
        response = cls.datalab_api_call(cls.get_url(cls.CATEGORY_AGE_RATE), params)
        shopping_response = ShoppingResponse.parse(response)

        return AgeRate.parse(shopping_response)

    @classmethod
    def datalab_api_call(cls, url: str, params: dict, path_params: str = None) -> dict:
        request_url = url if path_params is None else "{0}?{1}".format(url, urllib.parse.quote(path_params))
        data = urlencode(params).encode("utf-8")

        req = urllib.request.Request(request_url)
        req.add_header("Origin", "https://datalab.naver.com")
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("referer", "https://datalab.naver.com/shoppingInsight/sCategory.naver")

        with urllib.request.urlopen(req, data=data) as response:
            response_code = response.getcode()

            if response_code is 200:
                response_body = response.read()
                response_body_dict = json.loads(response_body.decode("utf-8"))
                logging.info(response_body_dict)

                return response_body_dict
            else:
                logging.error("error to request")

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
