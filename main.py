#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from datetime import datetime, timedelta

import pytz

from parser.Parser import Parser


def main():
    logging.getLogger().setLevel(logging.INFO)


    try:
        logging.info(sys.version)
    except ImportError as error:
        # Output expected ImportErrors.
        logging.error(error)
        # Include the name and path attributes in output.
        logging.error(f'error.name: {error.name}')
        logging.error(f'error.path: {error.path}')
    except Exception as exception:
        # Output unexpected Exceptions.
        logging.error(exception, False)


    etl_date = (datetime.now(pytz.timezone('Asia/Seoul')) - timedelta(days=1)).strftime('%Y-%m-%d')

    params = Parser().get_params("50001768,50001769", etl_date)
    age_rate_info_list = Parser().get_age_rate_info_list(params)
    logging.info(age_rate_info_list)

    click_trend_rate_info_list = Parser().get_click_trend_info_list(params)
    logging.info(age_rate_info_list)

    device_rate_info_list = Parser().get_device_rate(params)
    logging.info(age_rate_info_list)

    gender_rate_info_list = Parser().get_gender_rate(params)
    logging.info(age_rate_info_list)

    keyword_rank = Parser().get_keyword_rank(params)
    logging.info(keyword_rank)


if __name__ == "__main__":
    main()
