#_*_ coding: utf-8 _*_

import datetime
import logging.handlers
import os

import pytz

FMT_DATE_YYYYMMDD = '%Y%m%d'
LOG_FILE = "logs"

class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""
    def converter(self, timestamp):
        # dt = datetime.datetime.fromtimestamp(timestamp)
        tzinfo = pytz.timezone('Asia/Seoul')
        # return tzinfo.localize(dt)

        return datetime.datetime.now(tzinfo).strftime('%Y%m%d %H:%M:%S.%f')

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        # if datefmt:
        #     s = dt.strftime(datefmt)
        # else:
        #     try:
        #         s = dt.isoformat(timespec='milliseconds')
        #     except TypeError:
        #         s = dt.isoformat()
        return dt
# Singleton
class Logger(object):
    __single = None  # the one, true Singleton

    def __new__(classtype, *args, **kwargs):
        # Check to see if a __single exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __single objects
        if classtype != type(classtype.__single):
            classtype.__single = object.__new__(classtype, *args, **kwargs)
        return classtype.__single

    def __init__(self, name=None):

        # logger 인스턴스를 생성 및 로그 레벨 설정
        self.logger = logging.getLogger("crumbs")
        self.logger.setLevel(logging.DEBUG)
        self.__init_logger()

    @classmethod
    def instance(cls):
        if None == Logger.__single:
            Logger.__single = Logger()
        return Logger.__single

    def __init_logger(self):
        #  formmater 생성
        formatter = Formatter('[%(levelname)s|%(filename)s:%(lineno)s]%(asctime)s > %(message)s')

        # PATH
        cur = os.path.dirname(__file__)
        LOG_DIR = os.path.join(cur, '..', 'logs')

        if not os.path.isdir(LOG_DIR):
            os.mkdir(LOG_DIR)
        logFile = os.path.join(LOG_DIR, LOG_FILE)
        # fileHandler와 StreamHandler를 생성
        fileHandler = logging.handlers.TimedRotatingFileHandler(logFile, when="MIDNIGHT", interval=1, encoding="utf-8")
        fileHandler.suffix = FMT_DATE_YYYYMMDD
        streamHandler = logging.StreamHandler()

        # handler에 fommater 세팅
        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        # Handler를 logging에 추가
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)

ae_log = Logger.instance().logger

if __name__ == '__main__':
    ae_log.debug("hello world")
