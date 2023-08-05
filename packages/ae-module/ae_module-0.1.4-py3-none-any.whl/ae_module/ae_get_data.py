# _*_ coding: utf-8 _*_

import abc
import os

import pandas as pd
import pandas_flavor as pf

import networkx as nx
from memoization import cached
from .ae_db import ae_DataBase
from .ae_aws_s3 import AWSManager
from .ae_logger import ae_log
from .ae_util import (
                               ae_get_top_N_period_data_cache_path,
                               ae_get_topN_KRX_data_cache_path, ae_md5)
from .ae_util import precomputed_krx_holidays as holi_KRX
from .ae_util import bday_krx
from .ae_util import ae_is_KRX_on_time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TEMP = os.path.join(BASE_DIR, '..', 'temp')

@pf.register_dataframe_method
def explode(df: pd.DataFrame, column_name: str, sep: str):
    """
    For rows with a list of values, this function will create new
    rows for each value in the list
    """

    df["id"] = df.index
    wdf = (
        pd.DataFrame(df[column_name].str.split(sep).fillna("").tolist())
        .stack()
        .reset_index()
    )
    # exploded_column = column_name
    wdf.columns = ["id", "depth", column_name]  ## plural form to singular form
    # wdf[column_name] = wdf[column_name].apply(lambda x: x.strip())  # trim
    wdf.drop("depth", axis=1, inplace=True)

    return pd.merge(df, wdf, on="id", suffixes=("_drop", "")).drop(
        columns=["id", column_name + "_drop"]
    )

class ae_data_manager(metaclass=abc.ABCMeta):
    __single = None  # the one, true Singleton
    def __new__(classtype, *args, **kwargs):
        # Check to see if a __single exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __single objects
        if classtype != type(classtype.__single):
            classtype.__single = object.__new__(classtype, *args, **kwargs)
        return classtype.__single
    # _INSTANCE = None
    # _singleton_lock = threading.Lock()

    # @classmethod
    # def instance(cls):
    #     if not cls._INSTANCE:
    #         with cls._singleton_lock:
    #             cls._INSTANCE = cls('instance')
    #             ae_log.debug('new ae_data_manager instance created')
    #     return cls._INSTANCE
    @classmethod
    def instance(cls):
        if None == ae_data_manager.__single:
            ae_data_manager.__single = ae_data_manager()
            ae_log.debug('new ae_data_manager instance created')
        return ae_data_manager.__single

    def __init__(self, name=None):
        self.str_today = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
        self.df_ohlvcs = None # k, v : 종목코드, df_ohlcv 
        self.df_종목명_종목코드_등 = None # k, v : 종목코드, df_ohlcv 
        self.dic_종목코드_종목명 = None
        self.dic_종목명_종목코드 = None
        self.dic_종목코드_시장 = None
        # self.load_dicts_종목명_종목코드()

    @cached(ttl = 60 * 30)
    def date_possible_naver(self, date_ref):
        '''
        네이버 파싱한 table YYYYMMDD_daily_allstock_naver / 에서 받아옴
        param  : date_ref 
        return : date_ref
        '''
        return ae_DataBase().get_possible_date_naver(date_ref)

    @property
    def date_possible_naver_recent(self):
        return ae_DataBase().get_possible_date_naver()

    def get_df_topN_시총순(self, date_ref, N):
        aws_db = ae_DataBase()
        df = aws_db.get_topN_시총_from_daily_naver_raw(date_ref, N)
        return df
    
    def get_codes_topN시총_date(self, date_ref, N):
        '''
        해당날짜의 시가총액 상위종목 N 개 
        param  : date_ref
        return : list 종목코드들
        '''
        list_codes = (self.get_df_topALL_date(date_ref)
                    .sort_values('시가총액', ascending=False)
                    .head(N)
                    .종목코드.unique().tolist()
            )
        return list_codes 

    def get_top_N_period_source(self, date_ref, N_종목수 = 30, periods = 5) -> dict:
        dict_dfs = {}

        for date in pd.bdate_range(end=date_ref, periods=periods, holidays=holi_KRX, freq='C'):
            str_date = date.strftime('%Y%m%d')
            # _df = _get_topN_KRX_from_server(str_date, N_종목수)
            _df = self.get_topN_naver_from_server(str_date, N_종목수)
            dict_dfs[str_date] = _df
        df = pd.concat(dict_dfs)
        # print('header', df.columns)

        list_codes = df.종목코드
        # str_codes = ""
        # for code in list_codes:
        #     str_codes += code
        str_codes = ''.join(df.종목코드)
        return dict_dfs, list_codes, ae_md5(str_codes)

    # @cached(ttl=60*30) # 30분 cache
    def get_top_N_on_date_period(self, date_ref, N_종목수 = 30, periods = 5) -> dict: 
        '''
        get top30 data of specific date from mysql
        종목의 중복횟수 계산함
        param  : 기준일, 종목수, 기준일부터 기간 
        return : 기간 별 중복횟수 계산
                 60일 상승률 추가 --> 취소
        '''
        # print("getdata in")
        dict_dfs, list_codes, code_hash = self.get_top_N_period_source(date_ref, N_종목수, periods)
        ae_log.debug(f'{date_ref} TOP[{N_종목수}] codes = {list_codes} | MD5 = {code_hash}')

        pk_file = ae_get_top_N_period_data_cache_path(date_ref, code_hash, N_종목수, periods)
        # ae_log.debug(f'{date_ref} TOP[{N_종목수}] codes = {list_codes} | MD5 = {code_hash}')

        # if False:
        if os.path.exists(pk_file):
            df = pd.read_pickle(pk_file)
            
        else:
            df = pd.concat(dict_dfs)
            종목명_중복횟수 = (df.groupby('종목명')
                                .size()
                                .sort_values(ascending=False)
                                .to_dict()
                            )
            df.loc[:,'중복횟수'] = df.종목명.map(종목명_중복횟수)
            # df.to_datetime('확인일자')  확인일자 YYYYMMDD
            # 기간내의 종목들 ohlcv 저장 to dict
            # print(f'df size {df.shape}')
            # global df_ohlcv
            # list_codes = df.종목코드.unique()
            # df_ohlcv = _get_ohlcv_on_top30_periods(list_codes)
            # # 등락률 60일 추가
            # df_ohlcv = _add_등락률_60일(df_ohlcv).reset_index(drop=True)
            # assert '등락률_60일' in df_ohlcv.columns
            # ae_log.debug('add 등락률 finished')
            # # df_ohlcv.to_datetime('일자')
            # # df
            # df_ohlcv.to_datetime('일자')
            # df_ohlcv.loc[:,'일자'] = df_ohlcv.일자.dt.strftime('%Y%m%d')
            # df_merged = df.merge(df_ohlcv.loc[:,['code','일자','등락률_60일']],
            #                 how='left',
            #                 left_on=['종목코드','확인일자'],
            #                 right_on=['code','일자'],
            #                 # validate = 'one_to_one',
            #                 )
            # df_merged.to_pickle(pk_file)
            # manage_cache_data.add_cache_data(df, AWS_CONST.CACHE_DIR, pk_file)

        dic_dfs = {}
        for k, v in df.groupby('확인일자'):  # 확인일자 는 KRX꺼임
            dic_dfs[k] = v

        return dic_dfs

    def _add_등락률_60일(self, df_ohlcvs):
        df = (df_ohlcvs.groupby('code')
                        .apply(lambda df: df.add_column('등락률_60일',df.loc[:,'현재가'].pct_change(60)))
                        # .set_index(['code','일자'])
        )
        df.fillna(0)
        # print('등락률 60', df.head(61))
        return df

    @cached(ttl=60*10)
    def _get_topN_KRX_from_server(self, str_date, N = 30):
        pk_file = ae_get_topN_KRX_data_cache_path(str_date, N)

        if os.path.exists(pk_file):
            df = pd.read_pickle(pk_file)
        else:
            df = ae_DataBase().get_topN_from_KRX(str_date, N)
            if df.시가총액.iloc[0] > 1_000_000_000:
                    df.시가총액 = df.시가총액 / 100_000_000

            # 당일 18시 이후 일 경우에만 저장 ( 주간에는 계속 바뀜)
            # strToday = datetime.datetime.now(tz_seoul).strftime('%Y%m%d')
            # if strToday == str_date and datetime.datetime.now(tz_seoul).hour > 18:
            #     manage_cache_data.add_cache_data(df, AWS_CONST.CACHE_DIR, pk_file)
        return df

    def get_df_topN_date(self, date_ref, N):
        '''
        해당날짜의 top N 
        '''
        return self.get_topN_naver_from_server(date_ref, N)

    @cached(ttl=60)
    def get_df_topALL_date(self, date_ref):
        '''
        해당날짜의 top N 
        '''
        return self.get_topN_naver_from_server(date_ref, 3000)

    def get_codes_topN_date(self, date_ref, N=30):
        '''
        해당날짜의 상승률 상위종목 N 개 
        param  : date_ref
        return : list 종목코드들
        '''
        return self.get_df_topN_date(date_ref, N).종목코드.unique().tolist()

    def _get_codes_topN_date_period_raw(self, date_ref, N=30, period = 30):
        '''
        해당날짜의 상승률 상위종목 N 개 
        param  : date_ref
        return : pd.Series 종목코드들
        '''
        df_최신 = self.get_df_topALL_date(date_ref)
        df_과거 = self.get_df_topALL_date(pd.Timestamp(date_ref) - period * bday_krx)
        wdf = pd.merge(df_최신, df_과거, on='종목코드', suffixes=('_new','_old'))
        wdf['가격변동_period'] = (wdf.현재가_new - wdf.현재가_old)/wdf.현재가_old
        return (wdf
                .sort_values('가격변동_period', ascending=False)
                .head(N)
                .종목코드.to_list()
                )

    @cached(max_size=100, ttl=60*10)
    def get_codes_topN_date_period(self, date_ref, N=30, period = 30):
        '''
        해당날짜의 상승률 상위종목 N 개 / 수정주가 반영 
        param  : date_ref
        return : list 종목코드들
        '''
        # 관련종목 +20 정도 버퍼로 받음
        codes = self._get_codes_topN_date_period_raw(date_ref, N + 50, period) 
        df_ohlcv_multi = self.get_ohlcv_on_codes_periods_for_drawing(codes, period)

        codes = (df_ohlcv_multi.groupby('code')
                .apply(lambda df: df.set_index('일자')[['현재가']]
                                    .pct_change(len(df)-1)
                        )
                .dropna()
                .reset_index()
                .sort_values('현재가', ascending=False)
                .head(N).code.tolist()
                )
            
        return codes
    
    def load_dicts_종목명_종목코드(self):
        '''
        return : None
        '''
        aws_db = ae_DataBase()
        df = self.get_df_종목명_종목코드_등() #KIWOOM all_stock_info 에서 받음

        self.dic_종목코드_종목명 = df[['종목코드','종목명']].set_index('종목코드').to_dict()['종목명']
        self.dic_종목코드_시장 = df[['종목코드','시장']].set_index('종목코드').to_dict()['시장']
        self.dic_종목명_종목코드 = df[['종목코드','종목명']].set_index('종목명').to_dict()['종목코드']

    def dict_종목코드_종목명(self):
        pass

    @cached(ttl=60*10)
    def get_df_종목명_종목코드_등(self):
        '''
        종목코드 종목명 시장 정보 - 
        1. pykrx 로 시도
        2. all_stock_info 에서  from KIWOOM
        '''
        aws_db = ae_DataBase()
        if self.df_종목명_종목코드_등 is not None:
            return self.df_종목명_종목코드_등
        else:
            try:
                df = aws_db.get_df_종목명_종목코드_시장_pykrx()
            except:
                ae_log.error('Fail to fetch 종목코드_종목명_from_pykrx')
                df = aws_db.get_df_종목명_종목코드_시장_AE() #KIWOOM all_stock_info 에서 받음

            self.df_종목명_종목코드_등 = df
                
            return self.df_종목명_종목코드_등

    @cached(max_size=30, ttl=60*10)
    def get_topN_naver_from_server_cache_size(self, str_date, N = 30):
        '''
        네이버파싱 종목정보 반환
        서버에 저장된 날짜 확인후 없으면 제일 최신 날짜 선택함
        '''
        str_date = self.date_possible_naver(str_date)        
        # str_date = '20200324'
        df = ae_DataBase().get_topN_from_daily_naver_filtered(str_date, N)
        df.rename(columns={"날짜":"확인일자"}, inplace=True)
        assert '확인일자' in df.columns
        return df

    @cached(ttl=60 * 10) 
    def get_topN_naver_from_server_cache_time(self, str_date, N = 30):
        '''
        네이버파싱 종목정보 반환
        서버에 저장된 날짜 확인후 없으면 제일 최신 날짜 선택함
        '''
        str_date = self.date_possible_naver(str_date)        
        # str_date = '20200324'
        df = ae_DataBase().get_topN_from_daily_naver_filtered(str_date, N)
        df.rename(columns={"날짜":"확인일자"}, inplace=True)
        assert '확인일자' in df.columns
        return df
    
    def get_topN_naver_from_server(self, str_date, N = 30):
        if ae_is_KRX_on_time():
            return self.get_topN_naver_from_server_cache_time(str_date, N)
        else:
            return self.get_topN_naver_from_server_cache_size(str_date, N)
    @cached(ttl=60*60*12)
    def _get_관리종목(self, str_date): # ae_db.py 로 넘어가야 할 내용
        start = str_date
        # end = (pd.Timestamp(str_date) + pd.Timedelta('1d')).strftime('%Y%m%d')
        end = pd.Timestamp(str_date) + pd.Timedelta('1d')
        sql = f'select * from 관리종목_네이버 WHERE scrapetime between {start} and "{end}"'
        df_관리종목 = pd.read_sql_query(sql, ae_DataBase().get_db_stockmaster_con())
        return df_관리종목

    def get_저장목록_시총정보(self, con): # ae_db.py 로 넘어가야 할 내용
        '''
        서버에서 이미 계산된 아래 목록 받아와서 dataframe 으로 저장함 
            날짜, N_UNIV, N_ROLL
        self.df_DATE_N_UNIV_N_ROLL 
        '''
        df = pd.read_sql_query('show tables', con)
        # wdf = df.loc[df.iloc[:,0].str.contains('df_date_corr_ohlc')]
        wdf = df.loc[df.iloc[:,0].str.contains('시총정보')]
        # wdf = wdf.iloc[:,0].str.extract(
        #     'CUMUL_(?P<CUMUL>\d)_N_UNIV_(?P<N_UNIV>\d{2})_N_ROLL_(?P<N_ROLL>\d{2})_(?P<DATE>\d{8})'
        #     )
        # wdf = wdf.iloc[:,0].str.extract('시총정보_KRX_(?P<DATE>\d{8})')
        wdf = wdf.iloc[:,0].str.split('_', expand=True).rename(columns={2:'date'})
        wdf.date = pd.to_datetime(wdf.date)
        wdf.sort_values('date', ascending=False, inplace=True)
        wdf.dropna(how='all', inplace=True)
        return wdf

    # @cached(ttl=60*10) # 10 minute
    def _get_ohlcv_on_codes_periods(self, codes, period):
        '''
        df ohlcvs 
        날짜는 넉넉히 5개월로 동일하게
        return : pd.DataFrame
        '''

        period = str(period)+'D'
        start = (pd.Timestamp.today() - pd.Timedelta(period)).strftime('%Y%m%d')
        ae_log.debug(start)
        end = self.str_today
        ae_log.debug(end)
        codes = tuple(codes)
        df = ae_DataBase().get_specific_day_data_multi(codes , start_date = start, end_date=self.str_today)
        return df

    def _get_ohlcv_on_codes_periods_pykrx(self, codes, period):
        '''
        df ohlcvs - adjusted  from pykrx (naver)
        return : pd.DataFrame
        '''
        period = str(period)+'D'
        start = (pd.Timestamp.today() - pd.Timedelta(period)).strftime('%Y%m%d')
        ae_log.debug(start)
        end = self.str_today
        ae_log.debug(end)
        codes = tuple(codes)
        df = ae_DataBase().get_specific_day_data_multi_pykrx(codes , start_date = start, end_date=self.str_today)
        return df

    @cached(ttl=60*10, max_size=128)
    def get_ohlcv_on_codes_periods_for_drawing(self, codes, period = 180):
        return self._get_ohlcv_on_codes_periods_pykrx(codes, period)

    @cached(ttl=60*10) # 10 minute
    def get_ohlcv_on_codes_periods(self, codes, period = 180):
        '''
        df ohlcvs 
        날짜는 넉넉히 5개월로 동일하게
        오늘 장중 데이터는 다음에 받아서 추가 
        return : pd.DataFrame
        '''
        df =  self._get_ohlcv_on_codes_periods(codes, period)
        # df_오늘 = (self.get_df_topN_date(self.str_today, 3000)
        #             .filter_column_isin('종목코드', codes)
        #             .loc[:,['확인일자','현재가','시가','고가','저가','거래량','종목코드']]
        #             .transform_column('확인일자', 
        #                     lambda x: pd.Timestamp(x).to_pydatetime().date()
        #             )
        #             .rename_columns({'확인일자':'일자','종목코드':'code'})
        # )
        aws_db = ae_DataBase()
        df_오늘 = pd.DataFrame()
        try:
            for code in codes:
                df_오늘 = pd.concat([df_오늘, aws_db.get_ohlcv_from_daum(code,1)])

            df_오늘 = (df_오늘.rename(columns={'tradePrice': '현재가','openingPrice':'시가', 
                                            'highPrice': '고가','lowPrice':'저가', 
                                            'candleAccTradeVolume':'거래량', 
                                            'symbolCode':'code',
                                            'date': '일자'})
                    .loc[:,['일자','현재가','시가','고가','저가','거래량','code']]
                .transform_column('code', lambda x: x[1:])
                .transform_column('일자', lambda x: pd.Timestamp(x).to_pydatetime().date())
            )
        except Exception as e:
            ae_log.error('다음 증권정보 없음')
        
        df = pd.concat([df, df_오늘]).drop_duplicates(['일자','code'])
                           # )일자	현재가	시가	고가	저가	거래량	code       
        return df

    @cached(ttl = 60*60)
    def get_ebest_theme_date_recent(self):  #TODO data_path 
        '''
        최신 날짜 ebest 테마 받아옴
        param  :
        return : pd.DataFrame
        '''
        df = ae_DataBase().get_ebest_theme_most_recent()
        return df

    @cached(ttl=60*10, max_size =128)
    def get_ebest_theme_date(self, date_ref):  #TODO data_path 
        '''
        해당 날짜 ebest 테마 받아옴
        param  :
        return : pd.DataFrame
        '''
        df = ae_DataBase().get_ebest_theme_on_date(date_ref)
        return df

    def get_df_stock_info_from_theme_code(self, code_theme, date_ref):
        '''
        return : (테마이름, df 종목정보)
        '''
        # g_theme = self.get_g_theme_stocks(date_ref)
        pass

    def get_code_theme(self, date_ref):
        '''
        해당 날짜의 top30 종목들과 
        최신 테마 비교해서
        각 종목의 테마를 dictionary 로 

        return  : dict { code : [테마1, 테마2, etcs]}
        '''
        df = pd.concat(self.get_top_N_on_date_period(date_ref).copy()).reset_index(drop=True)
        df_theme = self.get_ebest_theme_date_recent()
        dic_종목코드_테마 = {}
        for code in df.종목코드.unique():
            dic_종목코드_테마[code] = \
            df_theme.loc[df_theme.종목코드.str.contains(code),'테마명'].tolist()

        return dic_종목코드_테마

    def get_theme_list_from_code_list(self, codes):
        '''
        종목코드 리스트 받아서,
        해당 종목코드의 테마들을
        리스트로 반환
        '''
        df_theme = self.get_ebest_theme_date_recent()
        theme_list = []

        df_sankey = pd.DataFrame()        

        for code in codes:
            tdf = pd.DataFrame()
            try:
                list_of_code = df_theme.loc[df_theme.종목코드.str.contains(code),'테마명'].tolist()
                if len(list_of_code) == 0:
                    tdf = pd.DataFrame({'target':['데이터 준비 중'], 'code':[code]})
                else :
                    tdf['target'] = df_theme.loc[df_theme.종목코드.str.contains(code),'테마명'].head(5)
                    tdf['code'] = code

            except:
                tdf['target'] = '테마 준비 중'
                tdf['code'] = code

            df_sankey = pd.concat([df_sankey, tdf], axis=0, sort=True)
            df_sankey['source'] = df_sankey.code.map(self.dic_종목코드_종목명)
            df_sankey['value'] = 1

        return df_sankey

    def get_code_theme_single_date(self, date_ref):
        '''
        해당 날짜의 top30 종목을 받아서 이에 대한  
        return  : dict
        '''
        # df = (_get_topN_KRX_from_server(date_ref, N=30)).reset_index(drop=True)
        df = (self.get_topN_naver_from_server(date_ref, N=30)).reset_index(drop=True)
        
        df_theme = self.get_ebest_theme_date_recent()
        dic_종목코드_테마 = {}
        for code in df.종목코드.unique():
            dic_종목코드_테마[code] = \
            df_theme.loc[df_theme.종목코드.str.contains(code),'테마명'].tolist()

        return dic_종목코드_테마
    
    def get_json_nodes_edges_FDG(self, date_ref):
        '''
        해당 날짜의 top30 종목에 대한 테마명, 테마 그룹
        param  : date_ref YYYYMMDD 
        return : json_nodes, json_links

        '''
        # 이베스트 theme group  날짜 있는지 확인 필요 #TODO

        aws_db = ae_DataBase()
        # df_theme = self.get_ebest_theme_date(date_ref) 
        df_theme = self.get_ebest_theme_date_recent() 

        df_테마명_종목코드 =df_theme.loc[:,['테마명','종목코드']].explode(column_name='종목코드', sep=';')
        df_테마명_종목명 =df_theme.loc[:,['테마명','종목명']].explode(column_name='종목명', sep=';')

        # 종목정보 filtering
        l_종목코드_top30 = self.get_codes_topN_date(date_ref, N=30)
        df_테마명_종목코드_filtered = df_테마명_종목코드.filter_column_isin(column_name='종목코드', iterable=l_종목코드_top30)

        # df_테마명_테마그룹_filtered
        date_ref_theme_group = aws_db.get_possible_date_theme_group(date_ref) 
        df_테마명_테마그룹 = pd.read_sql_table(f'theme_group_{date_ref_theme_group}', ae_DataBase().get_db_trading_con(), index_col='index')
        테마명_filtered = df_테마명_종목코드_filtered.테마명.unique()
        df_테마명_테마그룹_filtered = df_테마명_테마그룹.filter_column_isin('테마', 테마명_filtered)

        ## node
        wdf = (df_테마명_종목코드_filtered.loc[:,['종목코드']])
        wdf['group'] = 1
        # 종목중복 제거
        wdf = wdf.drop_duplicates('종목코드')
        wdf['종목명'] =wdf.종목코드.map(self.dic_종목코드_종목명)
        wdf = wdf.loc[:,['종목명','group']]
        wdf = wdf.rename(columns={'종목명':'id'})
        wdf_종목명 = wdf

        df_테마명_filtered = pd.DataFrame(테마명_filtered)
        df_테마명_filtered['group'] = 2
        wdf = df_테마명_filtered.rename(columns={0:'id'})
        wdf_테마명= wdf

        df_테마그룹_filtered = pd.DataFrame(df_테마명_테마그룹_filtered.테마그룹.unique())
        df_테마그룹_filtered['group']= 3
        wdf = df_테마그룹_filtered.rename(columns={0:'id'})
        wdf_테마그룹 = wdf

        df_nodes_filtered = pd.concat([wdf_종목명, wdf_테마명, wdf_테마그룹]).reset_index(drop=True)

        ## edges
        df_테마명_종목코드_filtered['종목명'] = df_테마명_종목코드_filtered.종목코드.map(self.dic_종목코드_종목명)
        df_테마명_종목명_filtered = df_테마명_종목코드_filtered.loc[:,['테마명','종목명']]
        df_edge_테마명_종목명 = df_테마명_종목명_filtered.rename(columns={'테마명':'source','종목명':'target'})
        df_edge_테마명_테마그룹 = df_테마명_테마그룹_filtered.rename(columns={'테마':'source','테마그룹':'target'})
        
        df_edge_filtered = pd.concat([df_edge_테마명_종목명, df_edge_테마명_테마그룹])
        df_edge_filtered['value']= 1
        df_edge_filtered = df_edge_filtered[['source','target','value']]

        ## to json
        json_nodes = df_nodes_filtered.to_json(orient='records', force_ascii=False)
        json_links = df_edge_filtered.to_json(orient='records', force_ascii=False)

        return json_nodes, json_links

    def _get_g_theme_stocks_date_recent(self):
        '''
        테마의 최신날짜 기준으로 종목정보 처리해서 nx.Graph 반환
        return  : undirected graph
        '''
        df_테마_raw = self.get_ebest_theme_date_recent().fillna('Sorry').drop_duplicates('테마코드')
        date_for_theme = df_테마_raw.일자.iloc[0]
        df_종목_raw = self.get_df_topALL_date(date_for_theme).fillna('Sorry')

        df_테마코드_종목코드 = (df_테마_raw
                                .loc[:,['테마코드','종목코드']]
                                .explode(column_name='종목코드', sep=';')
                    )
        g_테마_종목 = nx.from_pandas_edgelist(df_테마코드_종목코드, 
                                        source='종목코드',
                                        target='테마코드',
                                        # create_using = nx.DiGraph()
                                        )
                                               # df_테마_raw['node'] = df_테마_raw['테마코드'].astype(int)
        dic_테마코드_테마명_등 = (df_테마_raw
                        .loc[:,['테마코드','테마명','거래증가율','평균등락율', '대비등락율']]
                        .set_index('테마코드')
                        .to_dict(orient='index')
                        )               

        dic_종목코드_종목명_등 = (df_종목_raw
                        # .loc[:,['node','name','code','종목코드','종목명','pbr','per']]
                        .set_index('종목코드', drop=False)
                        .to_dict(orient='index')
                        )               

 
        nx.set_node_attributes(g_테마_종목, dic_테마코드_테마명_등)
        nx.set_node_attributes(g_테마_종목, dic_종목코드_종목명_등)

        return g_테마_종목        # node 정보추가 

    @cached(ttl=60*10)
    def get_df_ebest_theme_period(self, date_ref, period):
        aws_db = ae_DataBase()
        return aws_db.get_ebest_theme_most_recent_period(period=period)

    def load_df_ebest_theme_period(self, date_ref, period):
        aws_db = ae_DataBase()
        self.df_ebest_theme[date_ref] = aws_db.get_ebest_theme_most_recent_period(period=period)

    @cached(ttl=60*10)
    def get_df_theme_code_rolling_평균등락율_거래증가율(self, date_ref, period):
        '''
        테마코드 별 평균등락율의 rolling mean, 거래증가율 rolling max 계산
        rolling(period)
        
        example)

            테마코드	일자	평균등락율	거래증가율
        0	0003	2020-04-02	1.284	52.90
        1	0004	2020-04-02	1.766	22.12
        2	0007	2020-04-02	1.748	43.03
        3	0008	2020-04-02	2.232	112.95
        4	0009	2020-04-02	1.506	38.06
        ...	...	...	...	...
        201	0422	2020-04-02	1.376	41.95
        202	0427	2020-04-02	3.480	36.72
        203	0432	2020-04-02	3.628	1762.15
        204	0435	2020-04-02	3.916	95.87
        205	0436	2020-04-02	2.138	45.25
        '''
        df = self.get_df_ebest_theme_period(date_ref, period)
        wdf = (df.set_index(['일자','테마명'])
                    .groupby('테마코드')
                    .rolling(period)
                    .agg({'평균등락율': 'mean', '거래증가율':'max'})
                )
        return wdf.dropna().reset_index()

    def _get_g_theme_stocks_date_recent_period(self, date_ref):
        '''
        return  : undirected graph
        '''
        # 1. 날짜 있는 날짜 선택 3개 선택
        # 2. 날짜별로 graph 새로 만듬 
        # 3. 평균노들 만듬?

        # 테마별 - 일자 - 정보

        # df 그대로 이용
        # 테마 - 일자 - 3일평균등락률 등...
        # 테마 --> 3일평균  

        # df_테마_raw = self.get_ebest_theme_date_recent().fillna('Sorry').drop_duplicates('테마코드')
        # df_종목_raw = self.get_df_topN_date(date_ref, N = 3000).fillna('Sorry')

        # df_테마코드_종목코드 = (df_테마_raw
        #                         .loc[:,['테마코드','종목코드']]
        #                         .explode(column_name='종목코드', sep=';')
        #             )
        # g_테마_종목 = nx.from_pandas_edgelist(df_테마코드_종목코드, 
        #                                 source='종목코드',
        #                                 target='테마코드',
        #                                 # create_using = nx.DiGraph()
        #                                 )
        #                                        # df_테마_raw['node'] = df_테마_raw['테마코드'].astype(int)
        # dic_테마코드_테마명_등 = (df_테마_raw
        #                 .loc[:,['테마코드','테마명','거래증가율','평균등락율', '대비등락율']]
        #                 .set_index('테마코드')
        #                 .to_dict(orient='index')
        #                 )               

        # dic_종목코드_종목명_등 = (df_종목_raw
        #                 # .loc[:,['node','name','code','종목코드','종목명','pbr','per']]
        #                 .set_index('종목코드', drop=False)
        #                 .to_dict(orient='index')
        #                 )               

 
        # nx.set_node_attributes(g_테마_종목, dic_테마코드_테마명_등)
        # nx.set_node_attributes(g_테마_종목, dic_종목코드_종목명_등)

        # return g_테마_종목        # node 정보추가 
        pass
    
    def _get_g_theme_stocks_date(self, date_ref):
        '''
        return  : undirected graph
        '''
        df_테마_raw = self.get_ebest_theme_date(date_ref).fillna('Sorry').drop_duplicates('테마코드')
        df_종목_raw = self.get_df_topALL_date(date_ref).fillna('Sorry')

        df_테마코드_종목코드 = (df_테마_raw
                                .loc[:,['테마코드','종목코드']]
                                .explode(column_name='종목코드', sep=';')
                    )
        g_테마_종목 = nx.from_pandas_edgelist(df_테마코드_종목코드, 
                                        source='종목코드',
                                        target='테마코드',
                                        # create_using = nx.DiGraph()
                                        )
                                               # df_테마_raw['node'] = df_테마_raw['테마코드'].astype(int)
        dic_테마코드_테마명_등 = (df_테마_raw
                        .loc[:,['테마코드','테마명','거래증가율','평균등락율', '대비등락율']]
                        .set_index('테마코드')
                        .to_dict(orient='index')
                        )               

        dic_종목코드_종목명_등 = (df_종목_raw
                        # .loc[:,['node','name','code','종목코드','종목명','pbr','per']]
                        .set_index('종목코드')
                        .to_dict(orient='index')
                        )               

 
        nx.set_node_attributes(g_테마_종목, dic_테마코드_테마명_등)
        nx.set_node_attributes(g_테마_종목, dic_종목코드_종목명_등)

        return g_테마_종목        # node 정보추가 

    @cached(ttl=60*10, max_size=10)
    def get_g_theme_stocks(self, date_ref):
        '''
        param  : date_ref : cache때문에 넣음
        return  : undirected graph  
        '''
        # TODO : date_ref 에 테마가 없는경우, 최신 테마로 함. 
        ae_log.debug(f'g_theme on {date_ref}')
        g_테마_종목 = self._get_g_theme_stocks_date_recent() # date_ref 는 필요없음

        return g_테마_종목        # node 정보추가 

    def get_active_theme_from_code(self, date_ref, codes):
        '''
        param  : 종목코드 입력 iterable로..
        return : 테마코드 한개
        '''
        # 종목코드 : 연관테마반환
        g_테마_종목 = self.get_g_theme_stocks(date_ref)
        lis_theme_code = []
        lis_theme_name = []
        for code in codes:
            try:
                theme_related = g_테마_종목[code]
                if len(theme_related) == 0: # 테마 없을때
                    lis_theme_code.append('9999')
                    lis_theme_name.append('Unknown')
                elif len(theme_related) == 1: # 테마 1개 있을때
                    theme_code =  list(theme_related)[0]
                    theme_name =  list(theme_related)[0]
                
                    lis_theme_code.append(theme_code)
                else: # 여러 테마 있을때
                    df_roll = self.get_df_theme_code_rolling_평균등락율_거래증가율(date_ref, period=3)
                    theme_code =  (df_roll
                        .filter_column_isin('테마코드', theme_related)
                        .sort_values('평균등락율', ascending=False)
                        .iloc[0].테마코드)
                    lis_theme_code.append(theme_code)

            except KeyError:
                ae_log.error(f'종목 {code}의 테마가 없음')
                lis_theme_code.append('9999')

        return dict(zip(codes, lis_theme_code))

    def get_json_nodes_links_theme(self, date_ref):
        '''
        top30 종목 --> 테마간 연결
        종목당 테마가 여러가지인 경우, 
          - 테마 가지가 2개 이상이면 그대로 둠
          - 테마 가지가 모두 1개이면 제일 핫한거만 남김
        '''
        period = 3
        df_테마_raw = self.get_ebest_theme_date_recent().fillna('Sorry').drop_duplicates('테마코드')
        df_종목_raw = self.get_df_topN_date(date_ref, N = 3000).fillna('Sorry')

        df_테마코드_종목코드 = (df_테마_raw
                                .loc[:,['테마코드','종목코드']]
                                .explode(column_name='종목코드', sep=';')
                    )
        g_테마_종목 = nx.from_pandas_edgelist(df_테마코드_종목코드, 
                                        source='종목코드',
                                        target='테마코드',
                                        create_using = nx.DiGraph() )
        

        df_테마_raw['node'] = df_테마_raw['테마코드'].astype(int)
        df_테마_raw['name'] = df_테마_raw['테마명']
        print(df_테마_raw.columns)
        dic_테마코드_테마명_등 = (df_테마_raw
                        .loc[:,['node','name','테마코드','테마명','거래증가율','평균등락율', '대비등락율']]
                        .set_index('테마코드')
                        .to_dict(orient='index')
                        )               

        # df_종목_raw['node'] = df_종목_raw['종목코드'].astype(int)
        df_종목_raw['code'] = df_종목_raw['종목코드']
        df_종목_raw['name'] = df_종목_raw['종목명']
        dic_종목코드_종목명_등 = (df_종목_raw
                        # .loc[:,['node','name','code','종목코드','종목명','pbr','per']]
                        .set_index('종목코드')
                        .to_dict(orient='index')
                        )               

        # node 정보추가 
        nx.set_node_attributes(g_테마_종목, dic_테마코드_테마명_등)
        nx.set_node_attributes(g_테마_종목, dic_종목코드_종목명_등)

        codes_top30 = self.get_codes_topN_date(date_ref, 30)

        # g_top30과테마들 = g_테마_종목.subgraph(l_테마명+list(codes_top30))
        g_테마_종목_top30= g_테마_종목.edge_subgraph(g_테마_종목.edges(codes_top30))

        l_code_edge_2개이상 = [x for x, y in g_테마_종목_top30.nodes.data() 
            if x.isdigit() #TODO 종목코드 있는 놈만 잡는걸로 변경
            if g_테마_종목_top30.degree(x) > 1]

        # l_code_edge_2개이상

        l_삭제테마 = []
        for 종목코드 in l_code_edge_2개이상:
            연결테마들 = g_테마_종목_top30[종목코드]
            # 연결테마들 모두 degree 가 1인지 확인
            num_테마들연결합 = sum([g_테마_종목_top30.degree[테마] for 테마 in 연결테마들])

            if len(연결테마들) <= 1: 
                print(연결테마들)
                continue 

            # 연결테마들 모두 degree 가 1개 이하 --> 1개만 남김(거래증가율)
            # 삭제될 테마들모음
            if num_테마들연결합 == len(연결테마들): 
                print(연결테마들)
                df_roll = self.get_df_theme_code_rolling_평균등락율_거래증가율(date_ref, period)
                l_삭제테마_종목당 = (df_roll.filter_column_isin('테마코드', 연결테마들)
                                .sort_values('거래증가율', ascending=False)
                                .iloc[1:].테마코드.tolist()
                            )
                l_삭제테마.extend(l_삭제테마_종목당)
            # 어떤건 테마연결 여러개 있는 경우
            else:
                l_삭제테마_종목당 = [테마 for 테마 in 연결테마들 
                        if g_테마_종목_top30.degree[테마] == 1 ]
                l_삭제테마.extend(l_삭제테마_종목당)

        g_테마_종목_top30_trim = nx.DiGraph(g_테마_종목_top30)
        g_테마_종목_top30_trim.remove_nodes_from(l_삭제테마)

        # nodes edges 보내기
        i = 0
        for k in g_테마_종목_top30_trim.nodes:
            nx.set_node_attributes(g_테마_종목_top30_trim, {k:{'node': i}})
            i = i+1
        nodes = (pd.DataFrame(g_테마_종목_top30_trim
                    .nodes
                    .data())
                    .iloc[:,1]
        ).to_list()

        wdf_edges = nx.to_pandas_edgelist(g_테마_종목_top30_trim)#.astype(int)
        dic_g_index_node = dict(g_테마_종목_top30_trim.nodes.data('node'))
        wdf_edges.loc[:,['source','target']] = (
            wdf_edges.loc[:,['source','target']]
            .applymap(lambda x: dic_g_index_node[x])
        )
        wdf_edges['value'] = 5

        code_theme_list = wdf_edges.to_dict(orient='records')
        return nodes, code_theme_list

    @cached(ttl=60*10, max_size = 20)
    def load_g_corr(self, date_ref, N_days = 60):
        '''
        param  : date_ref YYYYMMDD
        param  : N : number of corr dates, default = 20 
        return : g_corr  nx graph object
        '''
        # date_ref = ae_DataBase().get_possible_date_corr(date_ref)
        date_ref = AWSManager.get_possible_date_corr_s3(date_ref)
        key_list = AWSManager.get_file_list_corr_deepgraph(date_ref)
        sr = pd.Series(key_list)
        if len(sr) == 0:
            ae_log.error(f'key list  : {key_list}')
            ae_log.error(f'key list is empty : on {date_ref}')
            return None
        if sr.str.contains(f'{date_ref}_N{N_days}').sum() == 0:
            ae_log.error('No g_corr : need to check')
            return None
        else:
            key = sr[sr.str.contains(f'{date_ref}_N{N_days}\.gpickle', regex=True)].iloc[0]
            filename_gpickle = key.split('/')[-1]
            ae_log.debug(f'gpickle name : {filename_gpickle}')
            local_file = os.path.join(PATH_TEMP, filename_gpickle)
            try:
                g_corr = nx.read_gpickle(local_file)
            except:
                ae_log.debug(f'local_file: {local_file}')
                # AWSManager.downloadfile(key, f'../temp/{filename_gpickle}')
                # g_corr = nx.read_gpickle(f'../temp/{filename_gpickle}')
                AWSManager.downloadfile(key, local_file) 
                g_corr = nx.read_gpickle(local_file)

        # gpickle_file = os.path.join(PATH_TEMP, f'corr_{date_ref}_N{n_base_data}.gpickle')
        return g_corr

    @cached(ttl = 60 * 60 * 24) # 24시간
    def get_corr_values(self, code, date_ref, period):
        '''
        종목의 corr 값이 가장 높은 것 5개 선택하기
        param  : code, date
        retrun : df_  column : corr, 종목코드
        '''
        ae_log.debug('start get g_corr')
        g_corr = self.load_g_corr(date_ref, period)
        ae_log.debug('done getting g_corr')
        
        if code in g_corr.nodes:
            neighbers_sorted = sorted(g_corr[code].items() , key=lambda edge: edge[1]['corr'], reverse=True)[0:4]
            # [code for code in neighbers_sorted if not in self.get_관리종목(date_ref)]
            list_node = [(n[0], n[1]['corr']) for n in neighbers_sorted]
            list_node.insert(0,(code, 1))
            code_list, corr_value_list = zip(*list_node)

        else:
            code_list, corr_value_list = [code], [1] 

        return code_list, corr_value_list

    def get_codes_from_all_theme_related(self, code, date_ref):
        '''
        종목코드와 연관된 테마들의 모든 종목코드 set 반환
        없으면 empty set
        한종목 --> 여러종목
        '''
        g_theme_stocks = self.get_g_theme_stocks(date_ref)
        if code in g_theme_stocks:
            return set([종목코드 
                            for 테마코드 in g_theme_stocks[code] 
                                for 종목코드 in g_theme_stocks[테마코드]])
        else:
            return set()

    def get_theme_code_multi_date(self, date_ref):
        '''
        해당날짜 바로 

        return  : dict(테마명: pd.DataFrame -- )
        '''
        
        df_theme = self.get_ebest_theme_date_recent()
        
        dic_테마_종목코드 = {}

        for index, row in df_theme.iterrows():
            df_name_code = pd.DataFrame()
            code_list = row.종목코드.split(';')
            name_list = list()

            for code in code_list:
                name = ae_DataBase().get_stock_name(code)
                name_list.append(name)

            df_name_code = pd.DataFrame(list(zip(name_list, code_list)), columns =['종목명', '종목코드'])

            dic_테마_종목코드[row.테마명] = df_name_code

        return dic_테마_종목코드

    def get_theme_rank_period(self, date_ref):
        '''
        input : 기준일
        output : 5일간의 테마 랭킹 (max : 30개)
        how : Top30 종목코드 -> 종목에 해당하는 테마들 -> 테마 반복 횟수 + 해당 종목 거래대금 합 -> Sorting -> dict 반환 
        '''

        #Top30 종목 코드(dict-> key:date, value:df)
        N_days_top_n = self.get_top_N_on_date_period(date_ref).copy()
        for date, df in N_days_top_n.items():
            N_days_top_n[date] = df[['종목코드', '종목명', '등락률', '거래대금']].reset_index(drop=True)

        #테마명 붙이기/반복횟수/거래대금합 
        df_theme = self.get_ebest_theme_date_recent()
    
        dic_theme_top30 = {}
        for date, df in N_days_top_n.items():
            df_theme_info = pd.DataFrame()
            for index, row in df.iterrows():
                code = row['종목코드']
                theme_list = df_theme.loc[df_theme.종목코드.str.contains(code),'테마명'].tolist()
                df_temp = pd.DataFrame(theme_list, columns=['테마명'])
                df_temp['종목코드'] = code
                df_temp['종목명'] = row['종목명']
                df_temp['등락률'] = row['등락률']
                df_temp['거래대금'] = row['거래대금'] / 100
                df_theme_info = pd.concat([df_theme_info, df_temp])
            
            종목수 = list()
            평균등락률 = list()
            전체거래대금 = list()
            테마명 = list()
            for theme, data in df_theme_info.groupby('테마명'):
                테마명.append(theme)
                종목수.append(data.shape[0])
                평균등락률.append(data['등락률'].mean())
                전체거래대금.append(data['거래대금'].sum())
            
            df_theme_calc = pd.DataFrame(list(zip(테마명, 종목수, 평균등락률, 전체거래대금)), columns=['테마명', '종목수', '평균등락률', '전체거래대금'])
            df_theme_calc = df_theme_calc.sort_values(by=['종목수', '전체거래대금', '평균등락률'], ascending=False).reset_index(drop=True)
            dic_theme_top30[date] = df_theme_calc.iloc[0:29]

        df = pd.concat(dic_theme_top30)
        theme_list_5days = df.테마명.unique()

        종목명_중복횟수 = (df.groupby('테마명')
                            .size()
                            .sort_values(ascending=False)
                            .to_dict()
                        )
        
        for k,v in dic_theme_top30.items():
            v.loc[:,'중복횟수'] = v.테마명.map(종목명_중복횟수)
            dic_theme_top30[k] = v


        
        return dic_theme_top30, theme_list_5days

    def get_kosi_kosdaq_period(self, date_ref, periods = 30):

        date_range = pd.bdate_range(end=date_ref, periods=periods, holidays=holi_KRX, freq='C')
        
        start_date = date_range[0].strftime("%Y%m%d")
        end_date = date_range[-1].strftime("%Y%m%d")

        df_kospi = ae_DataBase().get_specific_kospi_data(start_date, end_date)
        df_kosdaq = ae_DataBase().get_specific_kosdaq_data(start_date, end_date)
        
        return df_kospi, df_kosdaq

    def get_old_bdate(self, date_ref, period = 30):
        old_date = pd.Timestamp(date_ref) - period * bday_krx
        return old_date

# if __name__ == '__main__':
#     ae = ae_data_manager.instance()
#     ae.get_top_N_on_date_period('20191230')
