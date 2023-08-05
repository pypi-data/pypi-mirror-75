# -*- coding: utf-8 -*-
import abc
import datetime

from .ae_logger import ae_log
from .ae_telegram_constant import TELEGRAM_COMMAND
from .ae_util import tz_seoul


class dbCollectState():
    def __init__(self, db_name: str = "aws"):
        self.db_name = db_name
        self.time_stamp = datetime.datetime.now(tz_seoul).strftime("%Y-%m-%d %H:%M:%S")

class dbCollectStateManager(metaclass=abc.ABCMeta):
    __single = None  # the one, true Singleton
    def __new__(classtype, *args, **kwargs):
        # Check to see if a __single exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __single objects
        if classtype != type(classtype.__single):
            classtype.__single = object.__new__(classtype, *args, **kwargs)
        return classtype.__single

    def __init__(self, name=None):
        self.name = name
        self.map_db_state = {}

        for db in TELEGRAM_COMMAND:
            if db.value < TELEGRAM_COMMAND.CMD_DB_UPDATE_MAX.value:
                self.map_db_state[db.name] = None

    @classmethod
    def instance(cls):
        if None == dbCollectStateManager.__single:
            dbCollectStateManager.__single = dbCollectStateManager()
        return dbCollectStateManager.__single

    def update_state(self, tele_cmd: str, db_source: str):
        if tele_cmd in self.map_db_state:
            self.map_db_state[tele_cmd] = dbCollectState(db_source)

            self.notify()

    def notify(self):
        str_msg = ""
        for i, (k,v) in enumerate(self.map_db_state.items()):
            str_timestamp = ""
            success = False
            if v != None:
                str_timestamp = v.time_stamp
                success = True
            msg = f"{k.replace('CMD_DB_UPDATE_','')}|{success}|{str_timestamp}\n"
            str_msg = str_msg + msg
        ae_log.info(str_msg)
aeDbCollectorState = dbCollectStateManager.instance()

if __name__ == '__main__':

    print(aeDbCollectorState)