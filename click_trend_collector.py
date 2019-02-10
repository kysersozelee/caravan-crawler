import logging
import sys
from multiprocessing.pool import Pool

from db.DbConnector import DbConnector
from parser.Parser import Parser

logging.getLogger().setLevel(logging.INFO)


def collect_keyword_trend(cid, keyword, start_date="2017-08-01", end_date="2019-01-31"):
    params = Parser.get_params(cid, end_date=end_date, start_date=start_date)

    params['keyword'] = keyword

    shopping_param, click_trend_info_list = Parser().shopping_request(Parser.CATEGORY_CLICK_TREND, params,
                                                                      use_random_proxy=True)

    if len(click_trend_info_list) < 1:
        return

    click_trend_info_id = DbConnector().insert_info(table_name="click_trend_info",
                                                    shopping_param=shopping_param,
                                                    shopping_info_list=click_trend_info_list
                                                    )

    for age_rate_info in click_trend_info_list:
        DbConnector().insert_trend(click_trend_info_id, age_rate_info.data_list)


pool = Pool(processes=10)

if __name__ == "__main__":
    start_id = sys.argv[1]
    end_id = sys.argv[2]
    keyword_rank_list = DbConnector().select_distinct_keyword_rank(start_id, end_id)

    result = []
    for (cid, keyword) in keyword_rank_list:
        result.append((cid, keyword, "2017-08-01", "2019-01-31"))

    pool.starmap(collect_keyword_trend, result)
