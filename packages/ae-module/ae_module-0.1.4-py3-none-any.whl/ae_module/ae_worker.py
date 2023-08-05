# -*- coding: utf-8 -*-
import enum
import queue
import threading
import time

from .ae_collect_state import aeDbCollectorState
from .ae_logger import ae_log
from .ae_telegram_constant import TELEGRAM_CMD_SPLIT, TELEGRAM_COMMAND, TELEGRAM_ARG_SPLIT
from .ae_telegram_message import ae_tele_message

class JOB_CMOMMAND(enum.Enum):
    JOB_COMMAND_DUMMY = 0

    JOB_COMMAND_TELEGRAM_PROTOCOL = 100

class ae_job:
    def __init__(self, job_cmd:JOB_CMOMMAND, data = None):
        self.job_cmd = job_cmd
        self.data = data

lock = threading.Lock()

class ae_Worker:
    def __init__(self):
        self.msg_queue =queue.Queue()
        self.worker_handle = None
        self.req_stop = False
        self.__start_worker()

    def __start_worker(self):
        self.worker_handle = threading.Thread(target=self.__do_worker, args=())
        self.worker_handle.start()

    def __do_worker(self):
        ae_log.info('started worker')
        while self.worker_handle.isAlive():
            if self.msg_queue.qsize() > 0:
                lock.acquire()
                job = self.msg_queue.get()
                self.__handle_job(job)
                lock.release()

            if self.req_stop:
                break

            time.sleep(1)
        ae_log.info('stopped worker')

    def __handle_job(self, job: ae_job):
        ae_log.debug(job.job_cmd.name)

        if job.job_cmd == JOB_CMOMMAND.JOB_COMMAND_TELEGRAM_PROTOCOL:
            arr = job.data.split(TELEGRAM_CMD_SPLIT)
            tele_cmd = arr[1]
            tele_arg_count = int(arr[2])
            args = []
            if tele_arg_count:
                args = arr[3].split(TELEGRAM_ARG_SPLIT)

            ae_log.info(f'Received telegram cmd message = {tele_cmd}')
            if tele_arg_count < 1 or args[0] != "aws":
                ae_log.error(f'Received invalid arg = {tele_cmd}')
                return
            aeDbCollectorState.update_state(tele_cmd, args[0])
            if tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_KWDB_DAILY.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_KWDB_INVESTOR.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_KWDB_TOTAL.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_KWDB_MINUTE.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_WEB_KRX_MARKET1.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_WEB_KRX_MARKET2.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_WEB_NAVER_SISE.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_WEB_NAVER_MANAGER.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_EBEST.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_ORDER_BUY_STOCK.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DATA_UPDATE_CORREL.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_EBEST.name:
                pass
            elif tele_cmd == TELEGRAM_COMMAND.CMD_DB_UPDATE_WEB_DAUM_REPORTS.name:
                pass
            else:
                ae_tele_message.send_error(f'Received unhandled telegram cmd message = {tele_cmd}')

    def send_job(self, job: ae_job):
        lock.acquire()
        self.msg_queue.put(job)
        lock.release()

    def stop_worker(self):
        self.req_stop = True
        self.msg_queue.empty()
        self.worker_handle.join()

ae_worker = ae_Worker()

if __name__ == '__main__':
    time.sleep(1)
    new_job = ae_job(JOB_CMOMMAND.JOB_COMMAND_DUMMY, data='1')
    ae_worker.send_job(job=new_job)
    ae_worker.send_job(ae_job(JOB_CMOMMAND.JOB_COMMAND_DUMMY, "2"))
    ae_worker.send_job(ae_job(JOB_CMOMMAND.JOB_COMMAND_DUMMY, "3"))
    ae_worker.send_job(ae_job(JOB_CMOMMAND.JOB_COMMAND_DUMMY, "4"))
    ae_worker.send_job(ae_job(JOB_CMOMMAND.JOB_COMMAND_DUMMY, "5"))
    time.sleep(2)
    ae_worker.send_job(ae_job(JOB_CMOMMAND.JOB_COMMAND_DUMMY, "6"))
    ae_worker.send_job(ae_job(JOB_CMOMMAND.JOB_COMMAND_DUMMY, "7"))
    ae_worker.send_job(ae_job(JOB_CMOMMAND.JOB_COMMAND_DUMMY, "8"))
    ae_worker.send_job(ae_job(JOB_CMOMMAND.JOB_COMMAND_DUMMY, "9"))

    ae_worker.stop_worker()


