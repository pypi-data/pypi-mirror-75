# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

cur_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(cur_dir, '..', 'db.env')
if os.path.exists(env_file) is False:
    raise Exception(f'db env 파일이 없습니다. path = {env_file}')
load_dotenv(dotenv_path=env_file, encoding='utf-8')

DB_TRADING_DATA_BASE_NAME = os.getenv('KWDB_TRADING')
DB_DAILY_DATA_BASE_NAME = os.getenv('KWDB_DAILY')
DB_MINUTE_DATA_BASE_NAME = os.getenv('KWDB_MINUTE')
DB_INVESTOR_DATA_BASE_NAME = os.getenv('KWDB_INVESTOR')
DB_TELEGRAM_DATA_BASE_NAME = os.getenv('KWDB_TELEGRAM')
KWDB_STOCK_MASTER = os.getenv('KWDB_STOCK_MASTER')
NAVER_DAILY = os.getenv('NAVER_DAILY')
KWDB_INVESTOR_PROCESSED = os.getenv('KWDB_INVESTOR_PROCESSED')
KWDB_TEST = os.getenv('KWDB_TEST')

DB_ACCOUNT_DATA_BASE_NAME = 'KWDB_ACCOUNT_DSK'
DB_CALC_CORREL_DATA_BASE_NAME = 'CALC_CORREL'
