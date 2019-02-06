#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime

import pandas as pd
import pytz
import sqlalchemy as db
from MySQLdb._exceptions import Error
from sqlalchemy.exc import SQLAlchemyError

from data.category.Category import Category
from data.rank.keyword_rank.KeywordRank import KeywordRank
from data.shopping.ShoppingParam import ShoppingParam


class DbConnectorMeta(type):
    def __new__(mcs, name, bases, attrs):
        if "__init__" in attrs:
            ctor = attrs["__init__"]

            def init(cls):
                if not cls._inited:
                    ctor(cls)

            attrs["__init__"] = init
        return super().__new__(mcs, name, bases, attrs)


class DbConnector(metaclass=DbConnectorMeta):
    _instance = None
    _inited = False

    def __new__(cls):
        if DbConnector._instance is None:
            DbConnector._instance = super().__new__(cls)
        elif not isinstance(DbConnector._instance, cls):
            raise TypeError
        return DbConnector._instance

    def __init__(self):
        super().__init__()
        logging.getLogger().setLevel(logging.INFO)

        # TODO: db 정보 환경변수로 받기, cp 관련 설정 튜닝
        self._engine = db.create_engine('mysql://caravan:caravan@0.0.0.0:3308/caravan')
        self._connection = self._engine.connect()
        self._metadata = db.MetaData()
        self._inited = True

    def __del__(self):
        self._connection.close()

    def select(self, table_name):
        table = db.Table(table_name, self._metadata, autoload=True, autoload_with=self._engine)

        query = db.select([table])
        results = self._connection.execute(query).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()
        df.head(5)

    def insert_info(self, table_name: str, shopping_param: ShoppingParam, shopping_info_list: list):
        table = db.Table(table_name, self._metadata, autoload=True, autoload_with=self._engine)

        query = db.insert(table)
        values_list = []
        for idx, shopping_info in enumerate(shopping_info_list):
            values_list.append(
                {'cid': shopping_param.cid if not shopping_param.cid.find(",") else shopping_param.cid.split(",")[idx],
                 'code': shopping_info.code,
                 'title': shopping_info.title,
                 'full_title': shopping_info.full_title,
                 'date_range': shopping_param.date_range,
                 'etl_date': datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d')
                 }
            )

        try:
            result_proxy = self._connection.execute(query, values_list)

            if result_proxy.rowcount == 0:
                return None
            if result_proxy.rowcount == 1:
                return result_proxy.inserted_primary_key
            else:
                inserted_primary_keys = []
                first_pk = result_proxy.lastrowid
                for key in range(first_pk, first_pk + result_proxy.rowcount):
                    inserted_primary_keys.append(key)
                return inserted_primary_keys
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            logging.error("Error to execute query. query:{}, error:{}".format(query, error))
            return []
        except Error as e:
            logging.error("Error to execute query. query:%s" % query)
            return []

    def insert_rate(self, table_name: str, info_id: int, data_list: list):
        table = db.Table(table_name, self._metadata, autoload=True, autoload_with=self._engine)

        query = db.insert(table)
        values_list = []
        for data in data_list:
            values_list.append(
                {'info_id': info_id,
                 'code': data.code,
                 'label': data.label,
                 'ratio': data.ratio
                 }
            )
            pass

        try:
            result_proxy = self._connection.execute(query, values_list)
            if result_proxy.rowcount == 0:
                return None
            if result_proxy.rowcount == 1:
                return result_proxy.inserted_primary_key
            else:
                inserted_primary_keys = []
                first_pk = result_proxy.lastrowid
                for key in range(first_pk, first_pk + result_proxy.rowcount):
                    inserted_primary_keys.append(key)
                return inserted_primary_keys
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            logging.error("Error to execute query. query:{}, error:{}".format(query, error))
            return []
        except Error as e:
            logging.error("Error to execute query. query:%s" % query)
            return []

    def insert_category(self, category: Category):
        table = db.Table("category", self._metadata, autoload=True, autoload_with=self._engine)

        child_list = list(map(lambda child_category: child_category.cid, category.child_list))

        query = db.insert(table).values(id=category.cid,
                                        pid=category.pid,
                                        name=category.name,
                                        parent_path=category.parent_path,
                                        level=category.level,
                                        exps_order=category.exps_order,
                                        parents=category.parents,
                                        child_list=child_list,
                                        leaf=category.leaf,
                                        deleted=category.deleted,
                                        svc_use=category.svc_use,
                                        sblog_use=category.sblog_use,
                                        full_path=category.full_path
                                        )
        try:
            result_proxy = self._connection.execute(query)
            if result_proxy.rowcount == 0:
                return None
            if result_proxy.rowcount == 1:
                return result_proxy.inserted_primary_key
            else:
                inserted_primary_keys = []
                first_pk = result_proxy.lastrowid
                for key in range(first_pk, first_pk + result_proxy.rowcount):
                    inserted_primary_keys.append(key)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            logging.error("Error to execute query. query:{}, error:{}".format(query, error))
            return []
        except Exception as e:
            logging.error("Error to execute query. query:%s" % query)
            return []

    def insert_trend(self, table_name: str, info_id: int, data_list: list) -> int:
        table = db.Table(table_name, self._metadata, autoload=True, autoload_with=self._engine)

        query = db.insert(table)
        values_list = []
        for data in data_list:
            values_list.append(
                {'info_id': info_id,
                 'period': data.period,
                 'value': data.value
                 }
            )

        try:
            result_proxy = self._connection.execute(query, values_list)
            return result_proxy.rowcount
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            logging.error("Error to execute query. query:{}, error:{}".format(query, error))
            return -1
        except Error as e:
            logging.error("Error to execute query. query:%s" % query)
            return -1

    # TODO : range 추가
    def insert_rank(self, table_name: str, range: str, keyword_rank: KeywordRank):

        table = db.Table(table_name, self._metadata, autoload=True, autoload_with=self._engine)

        query = db.insert(table).values(rank=keyword_rank.rank,
                                        keyword=keyword_rank.keyword,
                                        link_id=keyword_rank.link_id,
                                        etl_date=datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d')
                                        )

        try:
            result_proxy = self._connection.execute(query)
            return result_proxy.inserted_primary_key
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            logging.error("Error to execute query. query:{}, error:{}".format(query, error))
            return []
        except Error as e:
            logging.error("Error to execute query. query:%s" % query)
            return []
