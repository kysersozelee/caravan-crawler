import logging
from multiprocessing.pool import Pool

from db.DbConnector import DbConnector
from parser.Parser import Parser

logging.getLogger().setLevel(logging.INFO)


def collect_rank(cid, start_date, end_date):
    params = Parser.get_params(cid, end_date=end_date, start_date=start_date)
    page = 1
    params['page'] = page
    keyword_rank_list = Parser().get_keyword_rank(params, use_random_proxy=True)
    if len(keyword_rank_list) < 2:
        return
    for keyword_rank in keyword_rank_list[1]:
        DbConnector().print_rank(keyword_rank=keyword_rank, cid=cid, end_date=end_date,
                                 start_date=start_date)


pool = Pool(processes=8)

if __name__ == "__main__":
    selected_category_list = DbConnector().select_category("category")

    result = []
    for category in selected_category_list:
        cid = category[0]
        if cid == 0:
            continue
        result.append((cid, "2017-08-01", "2017-08-31"))
        result.append((cid, "2017-09-01", "2017-09-30"))
        result.append((cid, "2017-10-01", "2017-10-31"))
        result.append((cid, "2017-11-01", "2017-11-30"))
        result.append((cid, "2017-12-01", "2017-12-31"))
        result.append((cid, "2018-01-01", "2018-01-31"))
        result.append((cid, "2018-02-01", "2018-02-28"))
        result.append((cid, "2018-03-01", "2018-03-31"))
        result.append((cid, "2018-04-01", "2018-04-30"))
        result.append((cid, "2018-05-01", "2018-05-31"))
        result.append((cid, "2018-06-01", "2018-06-30"))
        result.append((cid, "2018-07-01", "2018-07-31"))
        result.append((cid, "2018-08-01", "2018-08-30"))
        result.append((cid, "2018-09-01", "2018-09-31"))
        result.append((cid, "2018-10-01", "2018-10-30"))
        result.append((cid, "2018-11-01", "2018-11-31"))
        result.append((cid, "2018-12-01", "2018-12-30"))
        result.append((cid, "2019-01-01", "2019-01-31"))

    pool.starmap(collect_rank, result)
