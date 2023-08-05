# -*- coding: utf-8 -*-
import threading

from .ae_aws_s3 import AWSManager, LOCAL_ROOT
from .ae_logger import ae_log


def __do_handler_thread():
    # down file list
    AWSManager.download_all(LOCAL_ROOT, ['telegram_session'], skip_exist=True)

def start_cache_data_sync():
    ae_log.info('start_cache_data_sync')
    t = threading.Thread(target=__do_handler_thread, args=( ))
    t.start()
    return t

def add_cache_data(df, bucket_dir: str, cache_file_path:str):
    pass
    # 일단 AWS 포팅시 막음
    # df.to_pickle(cache_file_path)

    # if ae_useCelery():
    #     try:
    #         from ae_celery.tasks import add
    #         r1 = add.apply_async(("add_cache_data", (bucket_dir, cache_file_path)))
    #     except Exception as e:
    #         ae_log.exception(e)
    #         AWSManager.uploadfile(cache_file_path, bucket_dir)
    # else:
    #     AWSManager.uploadfile(cache_file_path, bucket_dir)
    