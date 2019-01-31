import json
import logging
import ssl
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import urlencode

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

ssl._create_default_https_context = ssl._create_unverified_context
logging.getLogger().setLevel(logging.INFO)


def open_api_call(url, params, path_params=None):
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


def get_params(cid, end_date, start_date="2017-08-01"):
    return {"cid": cid,
            "timeUnit": "date",
            "startDate": start_date,
            "endDate": end_date,
            "device": "pc,mo",
            "gender": "f,m",
            "age": "10,20,30,40,50,60",
            }


if __name__ == "__main__":
    params = get_params("50001768", "2019-02-01")

    click_trends = open_api_call(URLS.get(CATEGORY_CLICK_TREND), params)
    device_rate = open_api_call(URLS.get(CATEGORY_DEVICE_RATE), params)
    gender_rate = open_api_call(URLS.get(CATEGORY_GENDER_RATE), params)
    age_rate = open_api_call(URLS.get(CATEGORY_AGE_RATE), params)
    keyword_rank = open_api_call(URLS.get(CATEGORY_KEYWORD_RANK), params)
