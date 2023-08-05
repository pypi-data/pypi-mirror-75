# -*- coding: utf-8 -*-
from datetime import datetime
from io import BytesIO

import pandas as pd
import pymysql
import requests
import tqdm
from pandas.tseries.offsets import BDay
from functools import lru_cache
from sqlalchemy import create_engine
import mysql.connector as sql

from .ae_env_manager import AeEnvManager, AE_ENV_TYPE
from .ae_logger import ae_log
from .ae_telegram_constant import TELEGRAM_CHANNEL_ID_증시의신, TELEGRAM_CHANNEL_ID_공시정보, TELEGRAM_CHANNEL_ID_주식_공시알리미, TELEGRAM_CHANNEL_ID_아이투자_텔레그램
from .ae_telegram_message import ae_TelegramMessage
from .ae_util import ae_is_KRX_on_day
from .ae_util import precomputed_krx_holidays as holi_KRX
from .ae_util import get_possible_date

import unicodedata as ud
from pykrx import stock

# str_recent_BDay = (pd.datetime.today() + BDay(1)-BDay(1)).strftime('%Y%m%d')  # TODO : KRX calendar 추후 반영
str_recent_BDay = get_possible_date(pd.Timestamp.today(tz='Asia/Seoul'))

class ae_DataBase:
    def __init__(self, source='gb'):
        import os
        from dotenv import load_dotenv
        db_env_path = AeEnvManager.instance().get_env_path(AE_ENV_TYPE.AE_ENV_ALL)
        if os.path.exists(db_env_path):
            load_dotenv(dotenv_path=db_env_path, encoding='utf-8')

        self.server_name = source
        self.tele_msg = ae_TelegramMessage()

        self.DB_TRADING_DATA_BASE_NAME = os.getenv('KWDB_TRADING')
        self.DB_DAILY_DATA_BASE_NAME = os.getenv('KWDB_DAILY')
        self.DB_MINUTE_DATA_BASE_NAME = os.getenv('KWDB_MINUTE')
        self.DB_INVESTOR_DATA_BASE_NAME = os.getenv('KWDB_INVESTOR')
        self.DB_TELEGRAM_DATA_BASE_NAME = os.getenv('KWDB_TELEGRAM')
        self.KWDB_STOCK_MASTER = os.getenv('KWDB_STOCK_MASTER')
        self.NAVER_DAILY = os.getenv('NAVER_DAILY')
        self.KWDB_INVESTOR_PROCESSED = os.getenv('KWDB_INVESTOR_PROCESSED')
        self.KWDB_TEST = os.getenv('KWDB_TEST')

        self.DB_ACCOUNT_DATA_BASE_NAME = 'KWDB_ACCOUNT_DSK'
        self.DB_CALC_CORREL_DATA_BASE_NAME = 'CALC_CORREL'

        if source == 'aws':
            self.DB_ID = os.getenv('AWS_DB_ID')
            self.DB_PWD = os.getenv('AWS_DB_PWD')
            self.DB_ADDRESS = os.getenv('AWS_DB_ADDRESS')
            self.DB_PORT = os.getenv('AWS_DB_PORT')
            self.server_type = 0
        elif source == 'hc':
            self.DB_ID = os.getenv('HC_DB_ID')
            self.DB_PWD = os.getenv('HC_DB_PWD')
            self.DB_ADDRESS = os.getenv('HC_DB_ADDRESS')
            self.DB_PORT = os.getenv('HC_DB_PORT')
            self.server_type = 1
        elif source == 'ye':
            self.DB_ID = os.getenv('YE_DB_ID')
            self.DB_PWD = os.getenv('YE_DB_PWD')
            self.DB_ADDRESS = os.getenv('YE_DB_ADDRESS')
            self.DB_PORT = os.getenv('YE_DB_PORT')
            self.server_type = 0
        elif source == 'gb':
            self.DB_ID = os.getenv('AWS_DB_ID')
            self.DB_PWD = os.getenv('AWS_DB_PWD')
            self.DB_ADDRESS = os.getenv('GB_DB_ADDRESS')
            self.DB_PORT = os.getenv('AWS_DB_PORT')
            self.server_type = 1
        self.server_addr = self.DB_ADDRESS
        ## KWDB_TRADING (AWS)
        self.db_trading_connection = None
        self.db_trading_con = None

        ## KWDB_DAILY (AWS)
        self.db_daily_connection = None
        self.db_daily_con = None

        ## DAILY_NAVER (YE)
        self.db_daily_naver_connection = None
        self.db_daily_naver_con = None

        ## KWDB_MINUTE (AWS)
        self.db_minute_connection = None
        self.db_minute_con = None

        ## KWDB_TELEGRAM (AWS)
        self.db_telegram_connection = None
        self.db_telegram_con = None

        ## KWDB_INVESTOR (AWS)
        self.db_investor_connection = None
        self.db_investor_con = None

        ## KWDB_INVESTOR_PROCESSED (AWS)
        self.db_investor_processed_connection = None
        self.db_investor_processed_con = None

        ## KWDB_TEST (AWS)
        self.db_test_connection = None
        self.db_test_con = None

        ## KWDB_STOCK_MASTER (AWS)
        self.db_stockmaster_connection = None
        self.db_stockmaster_con = None

        ## CALC_CORREL (AWS)
        self.db_calc_correl_connection = None
        self.db_calc_correl_con = None

        ## KWDB_ACCOUNT (LOCAL)
        self.db_account_connection = None

        ## dataframe
        self.df_stock_master = pd.DataFrame() # KWDB_TRADING.all_stock_info
        self.df_stock_info = pd.DataFrame() # KWDB_STOCK_MASTER.상장법인정보
        self.dic_종목명_종목코드 = None #self.get_종목명_종목코드_from_KW() # 미리 종목명 종목코드 받을 필요없음
        # self.load_종목코드_시장()  # 미리 종목코드 시장 받을 필요 없음

        ## Trackdown missing datas
        self.missing_symbols = []
        self.missing_symbols_investor = []

    def __str__(self):
        return f'server = {self.server_name}\nADDRESS = {self.DB_ADDRESS}\nID = {self.DB_ID}'

    def get_db_trading_connection(self, cursor_type=pymysql.cursors.DictCursor):
        if None == self.db_trading_connection:
            self.db_trading_connection = sql.connect(host=self.DB_ADDRESS, database=self.DB_TRADING_DATA_BASE_NAME, port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')
        return self.db_trading_connection.cursor(cursor_type)

    def get_db_trading_con(self):
        if None == self.db_trading_con:
            self.db_trading_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                                .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.DB_TRADING_DATA_BASE_NAME),
                                                encoding='utf8',
                                                echo=False)
            self.db_trading_con.connect()
        return self.db_trading_con

    def get_db_correl_connection(self, cursor_type=pymysql.cursors.DictCursor):
        if None == self.db_calc_correl_connection:
            self.db_calc_correl_connection = sql.connect(host=self.DB_ADDRESS, database=self.DB_CALC_CORREL_DATA_BASE_NAME, port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')
        return self.db_calc_correl_connection.cursor(cursor_type)

    def get_db_correl_con(self):
        if None == self.db_calc_correl_con:
            self.db_calc_correl_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                                .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.DB_CALC_CORREL_DATA_BASE_NAME),
                                                encoding='utf8',
                                                echo=False)
            self.db_calc_correl_con.connect()
        return self.db_calc_correl_con

    def get_db_stockmaster_connection(self, cursor_type=pymysql.cursors.DictCursor):
        if None == self.db_stockmaster_connection:
            self.db_stockmaster_connection = sql.connect(host=self.DB_ADDRESS, database=self.KWDB_STOCK_MASTER,
                                                         port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')
        return self.db_stockmaster_connection.cursor(cursor_type)

    def get_db_stockmaster_con(self):
        if None == self.db_stockmaster_con:
            self.db_stockmaster_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                                    .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.KWDB_STOCK_MASTER),
                                                    encoding='utf8',
                                                    echo=False)
            self.db_stockmaster_con.connect()
        return self.db_stockmaster_con

    def get_db_daily_naver_con(self):
        if None == self.db_daily_naver_con:
            self.db_daily_naver_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                                    .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.NAVER_DAILY),
                                                    encoding='utf8',
                                                    echo=False)
            self.db_daily_naver_con.connect()
        return self.db_daily_naver_con

    def get_db_account_connection(self, cursor_type = pymysql.cursors.DictCursor):
        if None == self.db_account_connection:
            self.db_account_connection = sql.connect(host=self.DB_ADDRESS, database=self.DB_ACCOUNT_DATA_BASE_NAME, port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')
        return self.db_account_connection.cursor(cursor_type)

    def get_db_daily_connection(self):
        if None == self.db_daily_connection:
            self.db_daily_connection = sql.connect(host=self.DB_ADDRESS, database=self.DB_DAILY_DATA_BASE_NAME, port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')
        return self.db_daily_connection

    def get_db_daily_con(self):
        if None == self.db_daily_con:
            self.db_daily_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                              .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.DB_DAILY_DATA_BASE_NAME),
                                              encoding='utf8',
                                              echo=False)
            self.db_daily_con.connect()
        return self.db_daily_con

    def get_db_minute_connection(self, cursor_type=pymysql.cursors.DictCursor):
        if None == self.db_minute_connection:
            self.db_minute_connection = sql.connect(host=self.DB_ADDRESS, database=self.DB_MINUTE_DATA_BASE_NAME, port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')
        return self.db_minute_connection.cursor(cursor_type)

    def get_db_minute_con(self):
        if None == self.db_minute_con:
            self.db_minute_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                               .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.DB_MINUTE_DATA_BASE_NAME),
                                               encoding='utf8',
                                               echo=False)
            self.db_minute_con.connect()

        return self.db_minute_con

    def get_db_telegram_connection(self, cursor_type=pymysql.cursors.DictCursor):
        if None == self.db_telegram_connection:
            self.db_telegram_connection = sql.connect(host=self.DB_ADDRESS, database=self.DB_TELEGRAM_DATA_BASE_NAME, port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')

        return self.db_telegram_connection.cursor(buffered=True)

    def get_db_telegram_con(self):
        if None == self.db_telegram_con:
            self.db_telegram_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                                 .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.DB_TELEGRAM_DATA_BASE_NAME),
                                                 encoding='utf8',
                                                 echo=False)
            self.db_telegram_con.connect()
        return self.db_telegram_con

    def get_db_investor_connection(self, cursor_type=pymysql.cursors.DictCursor):
        if None == self.db_investor_connection:
            self.db_investor_connection = sql.connect(host=self.DB_ADDRESS, database=self.DB_INVESTOR_DATA_BASE_NAME, port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')

        return self.db_investor_connection.cursor(cursor_type)

    def get_db_investor_con(self):
        if None == self.db_investor_con:
            self.db_investor_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                                 .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.DB_INVESTOR_DATA_BASE_NAME),
                                                 encoding='utf8',
                                                 echo=False)
            self.db_investor_con.connect()
        return self.db_investor_con

    def get_db_investor_processed_connection(self, cursor_type=pymysql.cursors.DictCursor):
        if None == self.db_investor_processed_connection:
            self.db_investor_processed_connection = sql.connect(host=self.DB_ADDRESS, database='KWDB_INVESTOR_PROCESSED', port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')

        return self.db_investor_processed_connection.cursor(cursor_type)

    def get_db_investor_processed_con(self):
        if None == self.db_investor_processed_con:
            self.db_investor_processed_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                                           .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.KWDB_INVESTOR_PROCESSED),
                                                           encoding='utf8',
                                                           echo=False)
            self.db_investor_processed_con.connect()
        return self.db_investor_processed_con

    def get_db_test_connection(self, cursor_type=pymysql.cursors.DictCursor):
        if None == self.db_test_connection:
            self.db_test_connection = sql.connect(host=self.DB_ADDRESS, database=self.KWDB_TEST, port=self.DB_PORT, user=self.DB_ID, password=self.DB_PWD, charset='utf8')

        return self.db_test_connection.cursor(cursor_type)

    def get_db_test_con(self):
        if None == self.db_test_con:
            self.db_test_con = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                             .format(self.DB_ID, self.DB_PWD, self.DB_ADDRESS, self.DB_PORT, self.KWDB_TEST),
                                             encoding='utf8',
                                             echo=False)
            self.db_test_con.connect()
        return self.db_test_con

    def get_all_tables(self, server="aws"):
        if server == "aws":
            dbcur = self.get_db_trading_connection()
        else:
            dbcur = self.get_db_account_connection()
        table_names = []
        try:
            dbcur.execute("SELECT * FROM information_schema.tables WHERE TABLE_SCHEMA = '{}'".format(self.DB_TRADING_DATA_BASE_NAME))
            tables = dbcur.fetchall()
            for table in tables:
                table_names.append(table)
        except Exception as e:
            # gb_log.exception(e)
            self.tele_msg.send_exception(self.server_name)
        finally:
            dbcur.close()
        return table_names

    def get_my_stock_tables_from_db(self, accout_id, isVirtual):
        pre = 'MyStock_{}'.format(accout_id)
        post = '{}'.format('virtual' if isVirtual else 'real')
        my_stock_tables = []
        all_talbes = self.get_all_tables("harry")
        for each in all_talbes:
            table_name = each[2]
            if table_name.startswith(pre) and table_name.endswith(post):
                my_stock_tables.append(table_name)

        return my_stock_tables

    def get_my_stock_names(self, table_name):
        dbcur = self.get_db_trading_connection()
        codes = []
        items = None

        try:
            dbcur.execute("SELECT * FROM {}".format(table_name))
            items = dbcur.fetchall()
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
        finally:
            dbcur.close()

        if items:
            for item in items:
                codes.append(item[1])
        return codes

    def check_table_exist(self, tablename: str, db_name: str = None):
        if db_name == None:
            db_name = self.DB_TRADING_DATA_BASE_NAME
        result = False
        if db_name == self.DB_TRADING_DATA_BASE_NAME:
            dbcur = self.get_db_trading_connection()
        elif db_name == self.DB_ACCOUNT_DATA_BASE_NAME:
            dbcur = self.get_db_account_connection()
        elif db_name == self.DB_TELEGRAM_DATA_BASE_NAME:
            dbcur = self.get_db_telegram_connection()
        elif db_name == self.DB_DAILY_DATA_BASE_NAME:
            dbcur = self.get_db_telegram_connection()
        elif db_name == self.DB_MINUTE_DATA_BASE_NAME:
            dbcur = self.get_db_telegram_connection()
        elif db_name == self.DB_INVESTOR_DATA_BASE_NAME:
            dbcur = self.get_db_investor_connection()
        else:
            ae_log.error(f'db_name = {db_name} not implement.')
            dbcur = self.get_db_test_connection()

        str_sql = """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(tablename.replace('\'', '\'\''))
        try:
            dbcur.execute(str_sql)
            if dbcur.fetchone()[0] >= 1:
                result = True
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
        finally:
            dbcur.close()
            return result

    def check_item_exist(self, table_name: str, key: str, data: str):
        result = False
        dbcur = self.get_db_trading_connection()
        try:
            sql = f"SELECT COUNT(*) FROM {table_name} WHERE {key} = '{data}';"
            ae_log.debug(f'check_item_exist | {sql}')
            dbcur.execute(sql)
            num_count = dbcur.fetchone()[0]
            ae_log.debug(f'number of count {num_count}')
            if num_count >= 1:
                result = True
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
        finally:
            dbcur.close()
            return result

    def check_day_stock_exist(self, stock_code: str):
        table = 'opt10081_{}_tbl'.format(stock_code)
        return self.check_table_exist(table)

    def check_investor_info_exist(self):
        table = 'opt10060tbl'

    def check_minute_stock_exist(self, stock_code: str):
        table = 'opt10080_{}_tbl'.format(stock_code)
        return self.check_table_exist(table)

    def get_stock_master_data(self, tablename: str = 'all_stock_info'):
        con = self.get_db_trading_con()
        df_tmp = pd.read_sql_table(tablename, con)
        return df_tmp

    def get_stock_info_data_from_krx(self):
        con = self.get_db_stockmaster_con()
        df_tmp = pd.read_sql_table('상장법인정보', con)
        return df_tmp

    def get_ebest_theme(self, tablename: str = 'ebest_theme'):
        con = self.get_db_trading_con()
        df_tmp = pd.read_sql_table(tablename, con)
        return df_tmp

    def get_ebest_theme_on_date(self, date: str, tablename: str = 'ebest_theme' ):
        con = self.get_db_trading_con()
        str_sql = f'SELECT * FROM {tablename} WHERE 일자 BETWEEN {date} and {date}'
        df_tmp = pd.read_sql_query(str_sql, con)
        return df_tmp

    def get_ebest_theme_most_recent(self, tablename: str = 'ebest_theme'):
        df_tmp = self.get_ebest_theme()
        recent_date = df_tmp['일자'].max()
        df_tmp = df_tmp.filter_date('일자', recent_date)
        return df_tmp

    def get_stock_name(self, code: str):
        try:
            if len(self.df_stock_master) == 0:
                self.df_stock_master = self.get_stock_master_data()

            df_result = self.df_stock_master.loc[self.df_stock_master['종목코드'] == code]

            val = df_result['종목명']
            if len(val.values) > 0:
                return val.values[0]
            ae_log.error(f'ae_db.get_stock_name({code}) => empty, Check pleas.')

            return ""
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
            return ""

    def get_관리종목(self, str_date: str):
        start = str_date
        # end = (pd.Timestamp(str_date) + pd.Timedelta('1d')).strftime('%Y%m%d')
        end = pd.Timestamp(str_date) + pd.Timedelta('1d')
        sql = f'select * from 관리종목_네이버 WHERE scrapetime between {start} and "{end}"'
        df_관리종목 = pd.read_sql_query(sql, self.get_db_stockmaster_con())
        return df_관리종목

    def get_stock_code(self, name: str):
        try:
            if len(self.df_stock_master) == 0:
                self.df_stock_master = self.get_stock_master_data()

            df_result = self.df_stock_master.loc[self.df_stock_master['종목명'] == name]
            val = df_result['종목코드']
            if len(val.values) > 0:
                return val.values[0]

            if len(self.df_stock_info) == 0:
                self.df_stock_info = self.get_stock_info_data_from_krx()

            df_result = self.df_stock_info.loc[self.df_stock_info['회사명'] == name]
            val = df_result['종목코드']
            if len(val.values) > 0:
                return val.values[0]

            ae_log.error(f'ae_db.get_stock_code({name}) => empty, Check pleas.')
            return ""
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
            return ""

    def get_day_data(self, stock_code: str):
        table = 'opt10081_{}_tbl'.format(stock_code)
        con = self.get_db_daily_con()
        strSql = 'SELECT * FROM {} ORDER BY 일자 DESC;'.format(table)
        df_daily = pd.read_sql(strSql, con)

        return df_daily

    def get_minute_data(self, stock_code: str):
        con = self.get_db_minute_con()
        table = 'opt10080_{}_tbl'.format(stock_code)
        strSql = 'SELECT * FROM {} ORDER BY 체결시간 DESC;'.format(table)
        df_daily = pd.read_sql(strSql, con)

        return df_daily

    def get_specific_day_data(self, stock_code: str, start_date='19790719', end_date='21001231', order='asc'):
        '''
        param :
            start_date : YYYYMMDD, end_date : YYYYMMDD
        '''
        ae_log.debug(f"stock_code {stock_code}")
        con = self.get_db_daily_con()
        ae_log.debug(f"finish connection {con}")
        strSql = f'SELECT 일자, 현재가, 시가, 고가, 저가, 거래량 FROM opt10081_{stock_code}_tbl WHERE 일자 BETWEEN "{start_date}" AND "{end_date}" ORDER BY 일자 {order}'
        df_daily = pd.read_sql(strSql, con)
        return df_daily

    @lru_cache(maxsize=128)
    def get_specific_day_data_multi(self, symbols : tuple, **kwargs):
        ae_log.debug(f"symbols {symbols}")
        data = pd.DataFrame()
        for code in tqdm.tqdm(symbols):
            try:
                df = self.get_specific_day_data(code, **kwargs)
            except Exception as e:
                ae_log.exception(e)
                ae_log.error(f'missing db table : {code}')
                self.missing_symbols.append(code)
                continue
            if len(df) == 0:
                ae_log.error('missing', code)
            df['code'] = code
            if data.empty:
                data = df
            else:
                data = pd.concat([data, df])
        return data
    def get_specific_day_data_multi_pykrx_AWS(self, symbols, cache_local_folder=False, **kwargs):
            data  = pd.DataFrame()
            for code in tqdm.tqdm(symbols):
                try:
                    df = self.get_specific_day_data(code, start_date=kwargs['start_date'], end_date=kwargs['end_date'])
                except Exception as e:
                    ae_log.exception(e)
                    self.missing_symbols.append(code)
                df['code'] = code
                if data.empty:
                    data = df
                else:
                    data = pd.concat([data, df])
            return data                

    def get_specific_investor_data(self, stock_code: str, **kwargs):
        con = self.get_db_investor_con()
        end_date = kwargs['end_date'] if 'end_date' in kwargs else "2100-12-31"
        start_date = kwargs['start_date'] if 'start_date' in kwargs else "1979-07-19"
        order = kwargs['order'] if 'order' in kwargs else "asc"

        strSql = f'SELECT 일자, 종목코드, 현재가, 누적거래대금, 개인투자자, 외국인투자자, 기관계, 기타법인, 내외국인, 금융투자, 연기금등, 사모펀드, 투신, 국가, 기타금융, 은행, 보험 FROM opt10060_{stock_code}_tbl WHERE 종목코드 = "{stock_code}" AND 일자 BETWEEN "{start_date}" AND "{end_date}" ORDER BY 일자 {order}'

        df_daily = pd.read_sql(strSql, con)
        return df_daily

    def get_specific_investor_data_multi(self, symbols, **kwargs):
        data = pd.DataFrame()
        for code in tqdm.tqdm(symbols):
            try:
                df = self.get_specific_investor_data(code, **kwargs)
            except Exception as e:
                ae_log.exception(e)
                ae_log.error(f'missing investor db table : {code}')
                self.missing_symbols_investor.append(code)
                continue
            if len(df) == 0:
                ae_log.error('missing', code)
            df['code'] = code
            if data.empty:
                data = df
            else:
                data = pd.concat([data, df])
        return data

    def get_specific_minute_data(self, stock_code: str, **kwargs):
        con = self.get_db_minute_con()
        end_date = kwargs['end_date'] if 'end_date' in kwargs else "2100-12-31"
        start_date = kwargs['start_date'] if 'start_date' in kwargs else "1979-07-19"
        order = kwargs['order'] if 'order' in kwargs else "asc"
        start_time = kwargs['start_time'] if 'start_time' in kwargs else "09:00"
        end_time = kwargs['end_time'] if 'end_time' in kwargs else "15:20"
        verify = kwargs['verify'] if 'verify' in kwargs else False
        try:
            if end_date.lower() == 'desc' or end_date.lower() == 'asc':
                order = end_date
                end_date = ""
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)

        strSql = f'SELECT 체결시간, 현재가, 시가, 고가, 저가, 거래량 FROM opt10080_{stock_code}_tbl WHERE 체결시간 BETWEEN "{start_date}" AND "{end_date}" AND DATE_FORMAT(체결시간, "%%H:%%i") >= "{start_time}" AND DATE_FORMAT(체결시간, "%%H:%%i") < "{end_time}" ORDER BY 체결시간 {order}'
        # print(strSql)
        df_minute = pd.read_sql(strSql, con)

        return df_minute

    def get_specific_kospi_data(self, start_date, end_date="", order="DESC"):
        con = self.get_db_daily_con()
        if end_date.lower() == 'desc' or end_date.lower() == 'asc':
            order = end_date
            end_date = ""

        if len(end_date):
            strSql = 'SELECT 일자, 현재가, 시가, 고가, 저가, 거래량, 거래대금 FROM opt20006_001_tbl WHERE 일자 BETWEEN "{}" AND "{}" ORDER BY 일자 {}'.format(start_date, end_date, order)
        else:
            strSql = 'SELECT 일자, 현재가, 시가, 고가, 저가, 거래량, 거래대금 FROM opt20006_001_tbl WHERE 일자 >= "{}" ORDER BY 일자 {}'.format(start_date, order)
        df_kospi = pd.read_sql(strSql, con)
        return df_kospi

    def get_specific_kosdaq_data(self, start_date, end_date="", order="DESC"):
        con = self.get_db_daily_con()
        if end_date.lower() == 'desc' or end_date.lower() == 'asc':
            order = end_date
            end_date = ""

        if len(end_date):
            strSql = 'SELECT 일자, 현재가, 시가, 고가, 저가, 거래량, 거래대금 FROM opt20006_101_tbl WHERE 일자 BETWEEN "{}" AND "{}" ORDER BY 일자 {}'.format(start_date, end_date, order)
        else:
            strSql = 'SELECT 일자, 현재가, 시가, 고가, 저가, 거래량, 거래대금 FROM opt20006_101_tbl WHERE 일자 >= "{}" ORDER BY 일자 {}'.format(start_date, order)
        df_kospi = pd.read_sql(strSql, con)
        return df_kospi

    def delete_minute_data(self, stock_code: str):
        dbcur = self.get_db_minute_connection()
        strSql = 'DROP TABLE opt10080_{}_tbl'.format(stock_code)
        result = False
        try:
            dbcur.execute(strSql)
            result = True
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
        finally:
            dbcur.close()
            return result

    def check_minute_table_exist(self, stock_code: str):
        dbcur = self.get_db_minute_connection()
        result = False
        tablename = 'opt10080_{}_tbl'.format(stock_code)
        try:
            dbcur.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(tablename.replace('\'', '\'\'')))
            if dbcur.fetchone()[0] >= 1:
                result = True
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
        finally:
            dbcur.close()
            return result

    def update_index_table_daily(self, stock_code: str):
        dbcur = self.get_db_daily_connection()
        tablename = 'opt10081_{}_tbl'.format(stock_code)
        stt_sql = f"ALTER TABLE {tablename} ADD INDEX {'index_date'} ( {'일자'} ); "

        try:
            dbcur.execute(stt_sql)
            result = True
            # print(f'success create index table {stock_code}')
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
            result = False
        finally:
            dbcur.close()
            return result

    def update_index_table_minute(self, stock_code: str):
        dbcur = self.get_db_minute_connection()
        tablename = 'opt10080_{}_tbl'.format(stock_code)
        stt_sql = f"ALTER TABLE {tablename} ADD INDEX {'index_date'} ( {'체결시간'} ); "

        result = False
        try:
            dbcur.execute(stt_sql)
            result = True
            # print(f'success create index table {stock_code}')
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
        finally:
            dbcur.close()
            return result

    def get_stock_info(self, stock_name: str):
        con = self.get_db_trading_con()
        strSql = f'SELECT T1.*, T2.* from all_stock_info as T1, 상승률_네이버 as T2 where T1.종목명 = "{stock_name}" and T2.종목명 = "{stock_name}" ORDER BY T2.날짜 DESC LIMIT 1'

        df_stock_info = pd.read_sql(strSql, con)
        return df_stock_info

    def insert_telegram_raw_data(self, msg_index, channel_name, stock_name, stock_code, channel_id, date, raw_data):
        dbcur = self.get_db_telegram_connection()
        table_name = "test_channel"
        if channel_id == TELEGRAM_CHANNEL_ID_증시의신:
            table_name = "증시의신"
        elif channel_id == TELEGRAM_CHANNEL_ID_공시정보:
            table_name = "공시정보"
        elif channel_id == TELEGRAM_CHANNEL_ID_주식_공시알리미:
            table_name = "공시알리미"
        elif channel_id == TELEGRAM_CHANNEL_ID_아이투자_텔레그램:
            table_name = "아이투자"
        else:
            table_name = "test_channel"

        raw_data2 = raw_data.replace('"', '`')
        if self.server_type == 0:
            str_sql = f'INSERT INTO {table_name} (`Index`, `Channel Name`, `Stock Name`, `Stock Code`, `Channel ID`, `Date`, `Raw Data`) VALUES ("{msg_index}", "{channel_name}", "{stock_name}", "{stock_code}", "{channel_id}", "{date}", "`{raw_data2}`");'
        else:
            v = date.strftime('%Y-%m-%d %H:%M:%S')
            str_sql = f'INSERT INTO {table_name} (`Index`, `Channel Name`, `Stock Name`, `Stock Code`, `Channel ID`, `Date`, `Raw Data`) VALUES ("{msg_index}", "{channel_name}", "{stock_name}", "{stock_code}", "{channel_id}", "{v}", "`{raw_data2}`");'

        try:
            dbcur.execute(str_sql)
            self.db_telegram_connection.commit()
            result = True
            ae_log.debug(f'success insert data {channel_name}, {msg_index}, {date} in {table_name}(SERVER={self.server_addr})')
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
        finally:
            dbcur.close()

    def get_sepcific_telegram_data(self, channel_id, **kwargs):  # start_date, end_date="", order="DESC"):
        con = self.get_db_telegram_con()
        table_name = "test_channel"
        if channel_id == TELEGRAM_CHANNEL_ID_증시의신:
            table_name = "증시의신"
        elif channel_id == TELEGRAM_CHANNEL_ID_공시정보:
            table_name = "공시정보"
        elif channel_id == TELEGRAM_CHANNEL_ID_주식_공시알리미:
            table_name = "공시알리미"
        elif channel_id == TELEGRAM_CHANNEL_ID_아이투자_텔레그램:
            table_name = "아이투자"
        else:
            table_name = "test_channel"

        end_date = kwargs['end_date'] if 'end_date' in kwargs else "2100-12-31"
        start_date = kwargs['start_date'] if 'start_date' in kwargs else "2000-01-01"
        order = kwargs['order'] if 'order' in kwargs else "asc"
        specific_time = kwargs['specific_time'] if 'specific_time' in kwargs else ""
        key_word = kwargs['key_word'] if 'key_word' in kwargs else ""
        limit = kwargs['limit'] if 'limit' in kwargs else 0
        str_limit = ""
        if limit > 0:
            str_limit = f" LIMIT {limit}"
        if len(key_word):
            strSql = f'SELECT Date, `Index`, `Raw Data`, `Channel Name` FROM {table_name} WHERE `Raw Data` LIKE "%%{key_word}%%" ORDER BY Date {order}{str_limit}'

            # print(strSql)
            df_data = pd.read_sql(strSql, con)
            return df_data

        if len(specific_time):
            strSql = f'SELECT Date, `Index`, `Raw Data`, `Channel Name` FROM {table_name} WHERE Date = "{specific_time}"'
            df_data = pd.read_sql(strSql, con)
            return df_data

        if len(end_date):
            strSql = f'SELECT Date, `Index`, `Raw Data`, `Channel Name` FROM {table_name} WHERE Date BETWEEN "{start_date}" AND "{end_date}" ORDER BY Date {order}'
        else:
            strSql = f'SELECT Date, `Index`, `Raw Data`, `Channel Name` FROM {table_name} WHERE Date >= "{start_date}" ORDER BY Date {order}'
        df_data = pd.read_sql(strSql, con)
        return df_data

    def get_last_telegram_data(self, channel_id):
        con = self.get_db_telegram_con()
        table_name = "test_channel"
        if channel_id == TELEGRAM_CHANNEL_ID_증시의신:
            table_name = "증시의신"
        elif channel_id == TELEGRAM_CHANNEL_ID_공시정보:
            table_name = "공시정보"
        elif channel_id == TELEGRAM_CHANNEL_ID_주식_공시알리미:
            table_name = "공시알리미"
        elif channel_id == TELEGRAM_CHANNEL_ID_아이투자_텔레그램:
            table_name = "아이투자"

        strSql = f'SELECT Date, `Index`, `Raw Data`, `Channel Name` FROM {table_name} ORDER BY Date DESC LIMIT 1'
        df_data = pd.read_sql(strSql, con)
        return df_data

    def update_telegram_data(self, df, tele_channel_id):
        try:
            table_name = ""
            if tele_channel_id == TELEGRAM_CHANNEL_ID_공시정보:
                table_name = '공시정보'
            elif tele_channel_id == TELEGRAM_CHANNEL_ID_증시의신:
                table_name = '증시의신'
            elif tele_channel_id == TELEGRAM_CHANNEL_ID_주식_공시알리미:
                table_name = '공시알리미'
            elif tele_channel_id == TELEGRAM_CHANNEL_ID_아이투자_텔레그램:
                table_name = '아이투자'
            else:
                table_name = 'test_channel'

            exist_table = self.check_table_exist(table_name,  self.DB_TELEGRAM_DATA_BASE_NAME)

            df_new = df
            if exist_table:
                df_last = self.get_last_telegram_data(tele_channel_id)
                if not df_last.empty:
                    df_new = df.loc[(df['Index'] > df_last['Index'][0])]

            df_new.to_sql(table_name, self.get_db_telegram_con(), if_exists='append', index=df_new['Index'])
        except Exception as e:
            ae_log.exception(e)

    def get_종목명_종목코드_AWS(self):
        '''
        이걸 다시 database에 넣는건 너무 무의미함.  
        return : dataframe 종목명_종목코드_시장
        '''
        tablename = '종목명_종목코드_시장'
        try:  # 먼저 table 읽어보고
            con = self.get_db_trading_con()
            df_tmp = pd.read_sql_table(tablename, con=con, index_col='index')
            # print(len(df_tmp))
            return df_tmp
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)

    @lru_cache(maxsize=10)
    def get_상장법인정보_kind(self, str_date=str_recent_BDay, to_sql=True):
        '''
        web에서 받은거 , 저장해 놓고, 부를때 서버 찾아보고 없으면 추가
        param  : str 'YYYYMMDD'
        return : pd.DataFrame // 상장폐지종목도 포함됨
        '''
        ae_log.debug(f'get_상장법인정보_kind from KIND : {str_date}')

        def __get_from_kind_krx():
            '''
            kind.krx.co.kr 에서 받아옴
            return: df
            '''

            import urllib

            DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'
            MARKET_CODE_DICT = {
                'kospi': 'stockMkt',
                'kosdaq': 'kosdaqMkt',
                'konex': 'konexMkt'
            }

            def download_stock_codes(market=None, delisted=True):  # delisted True -> 상장폐지종목 포함됨
                params = {'method': 'download'}

                if market.lower() in MARKET_CODE_DICT:
                    params['marketType'] = MARKET_CODE_DICT[market]

                if not delisted:
                    params['searchType'] = 13

                params_string = urllib.parse.urlencode(params)
                request_url = urllib.parse.urlunsplit(['http', DOWNLOAD_URL, '', params_string, ''])

                df = pd.read_html(request_url, header=0)[0]
                df.종목코드 = df.종목코드.map('{:06d}'.format)

                return df

            try:
                df_kospi = download_stock_codes('kospi', delisted=True)
                df_kosdaq = download_stock_codes('kosdaq', delisted=True)
                df_konex = download_stock_codes('konex', delisted=True)

                df_kospi['시장'] = '코스피'
                df_konex['시장'] = '코넥스'
                df_kosdaq['시장'] = '코스닥'

                df_master = pd.concat([df_konex, df_kosdaq, df_kospi])
                df_master['상장일'] = pd.to_datetime(df_master['상장일'])
                df_master['조회일'] = pd.datetime.today().strftime('%Y%m%d')

                return df_master
            except Exception as e:
                self.tele_msg.send_exception(self.server_name)

        tablename = f'상장법인정보_{str_date}'
        try:  # 먼저 table 읽어보고
            con = self.get_db_stockmaster_con()
            df_tmp = pd.read_sql_table(tablename, con, index_col='index')
            # print(len(df_tmp))

        except Exception as e:  # 저장안된 경우, 저장하기
            ae_log.exception(e)
            # print('fail to load from SQL')
            try:
                df_tmp = __get_from_kind_krx()
                if df_tmp is None:
                    self.tele_msg.send_exception(self.server_name)
                    return None
                if len(df_tmp) > 0 and to_sql:
                    df_tmp.to_sql(tablename, con, if_exists='replace')
                    ae_log.debug(f'uploaded at 서버 :{self.db_stockmaster_con} ')
                else:
                    ae_log.error('목록없음 : maybe select another day')

            except Exception as e:
                self.tele_msg.send_exception(self.server_name)

        return df_tmp

    def get_시총정보_네이버(self, str_date_start=str_recent_BDay, str_date_end=str_recent_BDay):
        '''
        네이버 스크래핑 결과 받아오기, 종목코드가 없음

        return  : pd.DataFrame 시총정보
        '''
        con = self.get_db_daily_naver_con()

        ae_log.info(f'from 네이버스크래핑 시총정보 from {str_date_start} to {str_date_end}')
        str_date_start = pd.to_datetime(str_date_start).strftime('%Y-%m-%d')
        str_date_end = pd.to_datetime(str_date_end).strftime('%Y-%m-%d')
        dic_dfs = {}
        for date in pd.bdate_range(start=str_date_start, end=str_date_end, holidays=holi_KRX, freq = 'C'):
            str_date = date.strftime('%Y%m%d')
            sql_시총정보_상승률_네이버 = \
            f"select * from {str_date}_daily_allstock_naver"
            try:
                df = pd.read_sql_query(sql_시총정보_상승률_네이버, con)
                dic_dfs[str_date]=df
            except Exception as e:
                self.tele_msg.send_exception(self.server_name)
        df = pd.concat(dic_dfs)
        return df

    def get_시총정보_krx(self, date=str_recent_BDay, to_sql=True, from_sql=True):
        '''
        web에서 받은거 , 저장해 놓고, 부를때 서버 찾아보고 없으면 추가
        그날의 정보 없는경우 (ex 휴일) 그냥 경고 and return None

        param  : str 'YYYYMMDD'
        return : pd.DataFrame // 날짜별 시총정보 들어있음
        '''
        ae_log.info(f'from marketdata  시총정보 on {date}')
        if not ae_is_KRX_on_day(date):
            date = (pd.Timestamp(date) + BDay(1) - BDay(1)).strftime('%Y%m%d')
            ae_log.debug(f'휴일이므로 --> 그 {date} 로 ')
            return None

        def stock_master_price(date=None):
            if date == None:
                date = datetime.today().strftime('%Y%m%d')  # 오늘 날짜

            # tele_logger.debug('기준일:'+date+'_상장종목_시총_업데이트_시작')
            # STEP 01: Generate OTP
            gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
            gen_otp_data = {
                'name': 'fileDown',
                'filetype': 'xls',
                'url': 'MKD/04/0404/04040200/mkd04040200_01',
                'market_gubun': 'ALL',  # 시장구분: ALL=전체
                'indx_ind_cd': '',
                'sect_tp_cd': '',
                'schdate': date,
                'pagePath': '/contents/MKD/04/0404/04040200/MKD04040200.jsp',
            }

            r = requests.post(gen_otp_url, gen_otp_data, headers={})
            code = r.content  # 리턴받은 값을 아래 요청의 입력으로 사용.

            # STEP 02: download
            down_url = 'http://file.krx.co.kr/download.jspx'
            headers = {
                'Referer': 'http://marketdata.krx.co.kr/mdi',
                # 'Host' : 'marketdata.krx.co.kr'
            }
            down_data = {
                'code': code,
            }

            r = requests.post(down_url, down_data, headers=headers)
            df = pd.read_excel(BytesIO(r.content), header=0, thousands=',')

            if len(df) < 10:
                ae_log.error('row가 10개보다 적음_휴장일?')
            return df

        tablename = f'시총정보_KRX_{date}'
        try:  # 먼저 table 읽어보고
            con = self.get_db_stockmaster_con()
            df_tmp = pd.read_sql_table(tablename, con=con, index_col='index')
            # print(len(df_tmp))

        except Exception as e:
            self.tele_msg.send_exception(self.server_name)
            ae_log.error('fail to load from SQL... try to fetch from marketdata')
            try:
                df_tmp = stock_master_price(date)
                if len(df_tmp) > 0 and to_sql:
                    df_tmp.to_sql(tablename, con, if_exists='replace')
                    ae_log.info(f'uploaded at 서버 :{self.db_stockmaster_con} ')
                else:

                    ae_log.error('목록없음 : maybe select another day')

            except Exception as e:
                self.tele_msg.send_exception(self.server_name)
                ae_log.error('목록없음 : maybe select another day')
                return None
        df_tmp['확인일자'] = date

        return df_tmp

    def get_시총정보_AWS_from_krx(self, str_date):
        tablename = f'시총정보_KRX_{str_date}'
        try:  # 먼저 table 읽어보고
            con = self.get_db_stockmaster_con()
            df_tmp = pd.read_sql_table(tablename, con=con, index_col='index')
            # print(len(df_tmp))
            return df_tmp
        except Exception as e:
            self.tele_msg.send_exception(self.server_name)

    def get_시총정보_상장법인_krx_kind(self, date=str_recent_BDay, to_sql=False):
        '''
        merge 시총정보, 상장법인정보
        '''
        ae_log.info(f'from marketdata_kind  시총정보 on {date}')
        if not ae_is_KRX_on_day(date):
            ae_log.error(f'{date} 휴일이므로 --> return None')
            return None
            # date = (pd.Timestamp(date) + BDay(1) - BDay(1)).strftime('%Y%m%d')
            # print(f'휴일이므로 --> 그 전 {date} 로 ')

        df_상장법인정보 = self.get_상장법인정보_kind(to_sql=to_sql)
        df_시총정보 = self.get_시총정보_krx(date, to_sql=to_sql)
        df_종목마스터_시총정보_일자별 = pd.merge(
            df_상장법인정보, df_시총정보,
            left_on='종목코드', right_on='종목코드', how='inner'
        )

        # if len(df_종목마스터_시총정보_일자별) > 0 and to_sql:
        #     df_종목마스터_시총정보_일자별.to_sql(tablename, con, if_exists='replace')
        #     print(f'uploaded at 서버 :{self.db_stockmaster_con} ')
        return df_종목마스터_시총정보_일자별

    def get_시총정보_상장법인_네이버_kind(self, date=str_recent_BDay, to_sql=False):
        '''
        merge 시총정보, 상장법인정보
        '''
        ae_log.info(f'from 네이버_kind 시총정보 on {date}')
        if not ae_is_KRX_on_day(date):
            ae_log.debug(f'{date} 휴일이므로 --> return None')
            return None
            # date = (pd.Timestamp(date) + BDay(1) - BDay(1)).strftime('%Y%m%d')
            # print(f'휴일이므로 --> 그 전 {date} 로 ')

        df_상장법인정보 = self.get_상장법인정보_kind(to_sql=to_sql)
        df_시총정보 = self.get_시총정보_네이버(str_date_start=date, str_date_end=date)
        df_종목명_종목코드_시장 = self.get_종목명_종목코드_AWS()
        df_시총정보_종목코드 = pd.merge(
            df_시총정보, df_종목명_종목코드_시장[['종목명', '종목코드']],
            left_on='종목명', right_on='종목명', how='inner', suffixes=("", "_y")
        )
        df_종목마스터_시총정보_일자별 = pd.merge(
            df_상장법인정보, df_시총정보_종목코드,
            left_on='종목코드', right_on='종목코드', how='inner'
        )

        # if len(df_종목마스터_시총정보_일자별) > 0 and to_sql:
        #     df_종목마스터_시총정보_일자별.to_sql(tablename, con, if_exists='replace')
        #     print(f'uploaded at 서버 :{self.db_stockmaster_con} ')
        return df_종목마스터_시총정보_일자별

    def get_종목코드_시장(self, str_date=str_recent_BDay):
        '''
        param  : str_date YYYYMMDD
        return : dictionary key 종목코드, value 시장
        '''
        df = self.get_상장법인정보_kind()
        return df.set_index('종목코드')[['시장']].to_dict()['시장']

    def get_topN_from_KRX(self, str_date, N = 30):
        '''
        param  : str 날짜 (YYMMDD)
        return : df 
        '''
        table_name = f'시총정보_KRX_{str_date}'
        df = pd.read_sql_query(f'select * from {table_name} order by 등락률 DESC LIMIT {N+50}', self.get_db_stockmaster_con())
        df['시장'] = df.종목코드.map(self.종목코드_시장)

        # 코넥스 제외 코스닥 코스피만
        df = df[df.시장.isin(['코스피','코스닥'])] # 코넥스 제외
        # 관리종목 제외  
        list_관리종목 = self.get_관리종목(str_date).종목명.tolist()
        df = df[~df.종목명.isin(list_관리종목)]
        # ETN 스팩 종목 제외
        df = df.query('~종목명.str.contains("ETN|스팩|스펙")', engine='python')
        # 우선주 제외 보통주 만
        df = df[df.종목코드.str.endswith('0')]     
        
        df = df.clean_names()  # column name --> lower case and add _ on space
        normalized_col_name = []
        for name in df.columns:
            normalized_col_name.append(ud.normalize('NFC', name))
        df.columns = normalized_col_name

        # if df.시가총액.iloc[0] > 1_000_000_000:
        #         df.시가총액 = df.시가총액 / 100_000_000
        df = df.sort_values('등락률', ascending=False).head(30)
        ae_log.debug(df.shape)
        return df

    def get_topN_from_daily_naver(self, str_date, N = 30):
        '''
        daily naver 에서 parsing 한 내용 받아오기
        관리종목 제외
        코넥스 제외
        ETN 스팩 종목 제외
        우선주 제외?
        '''
        table_name = f'{str_date}_daily_allstock_naver'
        str_sql = f'select * from {table_name} order by 등락률 DESC LIMIT {N+20}'
        df = pd.read_sql_query(str_sql, self.get_db_daily_naver_con())
        # 종목명 종목코드 붙이기 -- 네이버 원래 페이지에는 종목코드 없음 
        df['종목코드'] = df.종목명.map(self.종목명_종목코드)
        df['시장'] = df.종목코드.map(self.종목코드_시장)

        # 코넥스 제외 코스닥 코스피만
        df = df[df.시장.isin(['코스피','코스닥'])] # 코넥스 제외
        # 관리종목 제외  
        list_관리종목 = self.get_관리종목(str_date).종목명.tolist()
        df = df[~df.종목명.isin(list_관리종목)]
        # ETN 스팩 종목 제외
        df = df.query('~종목명.str.contains("ETN|스팩|스펙")', engine='python')
        # 우선주 제외 보통주 만
        df = df[df.종목코드.str.endswith('0')]     
        
        df = df.clean_names()  # column name --> lower case and add _ on space
        normalized_col_name = []
        for name in df.columns:
            normalized_col_name.append(ud.normalize('NFC', name))
        df.columns = normalized_col_name

        # if df.시가총액.iloc[0] > 1_000_000_000:
        #         df.시가총액 = df.시가총액 / 100_000_000
        df.drop_duplicates('종목코드', inplace=True)
        df = df.sort_values('등락률', ascending=False).head(30)

        # 종목코드 붙이기 (네이버 시총 사이트에는 없음)
        return df

    def load_관리종목(self, str_date):
        self.관리종목 = {}
        self.관리종목[str_date] = self.get_관리종목(str_date)

    def load_종목코드_시장(self ):
        self.종목코드_시장 = {}
        self.종목코드_시장 = self.get_종목코드_시장()

    def load_종목명_종목코드_from_KRX(self, str_date):
        ''' load 종목명-종목코드 from KRX parsing 결과
        '''
        pass

    def get_종목명_종목코드_from_KW(self):
        ''' load 종목명-종목코드 from KRX parsing 결과
        return  : dictionary 종목명 , 종목코드
        '''
        if len(self.df_stock_master) == 0:
            self.df_stock_master = self.get_stock_master_data()
        return self.df_stock_master.set_index('종목명').loc[:,'종목코드'].to_dict()

    def _get_possible_date(self, df, date = None):
        '''
        param  :    df 저장날짜 있는거, 확인가능 
                    date
        return : db에 있는 가능한 최신 날짜
        '''
        df = df.copy()
        if date is None:
            date = pd.Timestamp.today(tz='Asia/Seoul') 
        ae_log.debug(f'get_possible_date called, date to check : {date}')
            
        # if (df.DATE == date).sum() >= 1 :
        #     print(f'there is data on the date:{date}')
        #     str_date  = date.strftime('%Y%m%d')
        # else:
        ae_log.debug(f'there is no data on the date:{date}, looking for nearest')
        # 데이터가 없으면 제일 가까운 날짜 불러옴
        df.set_index('date', inplace=True)            
        date_nearest = df.index[df.index.get_loc(pd.to_datetime(date), method='nearest')]
        str_date = date_nearest.strftime('%Y%m%d')
        ae_log.debug(f'possible date is {str_date}')
        return str_date

    def get_저장목록_시총정보_daily_naver(self):
        '''
        서버에서 이미 계산된 아래 목록 받아와서 dataframe 으로 저장함 
            날짜, N_UNIV, N_ROLL
        self.df_DATE_N_UNIV_N_ROLL 
        '''
        con = self.get_db_daily_naver_con()
        df = pd.read_sql_query('show tables', con)
        wdf = df.loc[df.iloc[:,0].str.contains('daily')]
        # wdf = wdf.iloc[:,0].str.extract(
        #     'CUMUL_(?P<CUMUL>\d)_N_UNIV_(?P<N_UNIV>\d{2})_N_ROLL_(?P<N_ROLL>\d{2})_(?P<DATE>\d{8})'
        #     )
        # wdf = wdf.iloc[:,0].str.extract('시총정보_KRX_(?P<DATE>\d{8})')
        wdf = wdf.iloc[:,0].str.split('_', expand=True).rename(columns={0:'date'})
        wdf.date = pd.to_datetime(wdf.date)
        wdf.sort_values('date', ascending=False, inplace=True)
        wdf.dropna(how='all', inplace=True)
        wdf.drop_duplicates('date', inplace=True)
        return wdf

    def get_저장목록_시총정보(self, con):
        pass
        # '''
        # 서버에서 이미 계산된 아래 목록 받아와서 dataframe 으로 저장함 
        #     날짜, N_UNIV, N_ROLL
        # self.df_DATE_N_UNIV_N_ROLL 
        # '''
        # df = pd.read_sql_query('show tables', con)
        # # wdf = df.loc[df.iloc[:,0].str.contains('df_date_corr_ohlc')]
        # wdf = df.loc[df.iloc[:,0].str.contains('시총정보')]
        # # wdf = wdf.iloc[:,0].str.extract(
        # #     'CUMUL_(?P<CUMUL>\d)_N_UNIV_(?P<N_UNIV>\d{2})_N_ROLL_(?P<N_ROLL>\d{2})_(?P<DATE>\d{8})'
        # #     )
        # # wdf = wdf.iloc[:,0].str.extract('시총정보_KRX_(?P<DATE>\d{8})')
        # wdf = wdf.iloc[:,0].str.split('_', expand=True).rename(columns={2:'date'})
        # wdf.date = pd.to_datetime(wdf.date)
        # wdf.sort_values('date', ascending=False, inplace=True)
        # wdf.dropna(how='all', inplace=True)
        # return wdf


    def get_possible_date_naver(self, date : str = None):
        df_저장정보 = self.get_저장목록_시총정보_daily_naver()
        str_date = self._get_possible_date(df_저장정보, date) 
        return str_date

    def get_topN_from_daily_naver_filtered(self, str_date, N = 30):
        '''
        daily naver 에서 parsing 한 filter
        관리종목 제외
        코넥스 제외
        ETN 스팩 종목 제외
        우선주 제외?
        '''
        df = self.get_topN_from_daily_naver_raw(str_date, N)
        # 종목명 종목코드 붙이기 -- 네이버 원래 페이지에는 종목코드 없음 
        if self.dic_종목명_종목코드 is None:
            self.load_dic_종목명_종목코드_시장()
        df['종목코드'] = df.종목명.map(self.dic_종목명_종목코드)
        df['시장'] = df.종목코드.map(self.dic_종목코드_시장)
        
        # 코넥스 제외 코스닥 코스피만
        df = df[df.시장.isin(['KOSPI','KOSDAQ'])] # 코넥스 제외
        # 관리종목 제외  
        list_관리종목 = self.get_관리종목(str_date).종목명.tolist()
        # df = df[~df.종목명.isin(list_관리종목)]
        # ETN 스팩 종목 제외
        df = df.query('~종목명.str.contains("ETN|스팩|스펙")', engine='python')
        # 우선주 제외 보통주 만
        df = df[df.종목코드.str.endswith('0')]     
        df = df.clean_names()  # column name --> lower case and add _ on space
        normalized_col_name = []
        for name in df.columns:
            normalized_col_name.append(ud.normalize('NFC', name))
        df.columns = normalized_col_name

        # if df.시가총액.iloc[0] > 1_000_000_000:
        #         df.시가총액 = df.시가총액 / 100_000_000
        df.drop_duplicates('종목코드', inplace=True)
        df = df.sort_values('등락률', ascending=False).head(N)
        ae_log.debug(f'df.shape : {df.shape}')

        return df

    def load_dic_종목명_종목코드_시장(self):
        '''
        '''
        self.dic_종목코드_종목명, self.dic_종목코드_시장, self.dic_종목명_종목코드 =\
             self.get_dic_종목명_종목코드_시장() 
    def get_topN_from_daily_naver_raw(self, str_date, N):
        '''
        daily naver 에서 db값 그대로 parsing 내용 받아오기
        '''
        table_name = f'{str_date}_daily_allstock_naver'
        str_sql = f'select * from {table_name} order by 등락률 DESC LIMIT {N+100}'
        df = pd.read_sql_query(str_sql, self.get_db_daily_naver_con())
        # 종목명 종목코드 붙이기 -- 네이버 원래 페이지에는 종목코드 없음 
        return df

    def get_dic_종목명_종목코드_시장(self):
        try:
            df = self.get_df_종목명_종목코드_시장_pykrx()
            if df.empty:
                df = self.get_df_종목명_종목코드_시장_AE()
        except Exception as e:
            df = self.get_df_종목명_종목코드_시장_AE()

        dic_종목코드_종목명 = df.loc[:,['종목코드','종목명']].set_index('종목코드').to_dict()['종목명']
        dic_종목코드_시장 = df.loc[:,['종목코드','시장']].set_index('종목코드').to_dict()['시장'] 
        dic_종목명_종목코드 = df.loc[:,['종목코드','종목명']].set_index('종목명').to_dict()['종목코드'] 

        return dic_종목코드_종목명, dic_종목코드_시장, dic_종목명_종목코드 

    def get_df_종목명_종목코드_시장_AE(self):
        '''
        '''
        # 종목코드- 시장 
        df1 = self.get_상장법인정보_kind().replace({'코스피':'KOSPI', '코스닥':'KOSDAQ', '코넥스':'KONEX'})[['회사명','종목코드','시장']] # 회사명, 종목코드, 시장 not 종목명.
        # 종목코드 - 종목명
        df2 = self.get_stock_master_data()[['종목코드','종목명']]
        # merge
        df = pd.merge(df1,df2, left_on='종목코드',right_on='종목코드')

        return df

# aws_db = None
# hc_db = None
# gb_db = None
#
# try:
#     gb_db = ae_DataBase("gb")
# except Exception as e:
#     print(e)
#     # gb_db.tele_msg.send_exception("gb")
# try:
#     aws_db = ae_DataBase("aws")
# except Exception as e:
#
#     aws_db.tele_msg.send_exception("aws")
# # try:
# #     hc_db = ae_DataBase("hc")
# # except Exception as e:
# #     aws_db.tele_msg.send_exception("hc")
#
# def get_ae_db():
#     db = []
#     if aws_db != None :
#         db.append(aws_db)
#     if hc_db != None :
#         db.append(hc_db)
#     if gb_db != None :
#         db.append(gb_db)
#     return db
#
# if __name__ == '__main__':
#     dbs = get_ae_db()
#     for db in dbs:
#         ae_log.debug(f'db = {db}')