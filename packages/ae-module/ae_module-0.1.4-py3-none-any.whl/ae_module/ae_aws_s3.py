# -*- coding: utf-8 -*-

import os
import threading
import io

import pandas as pd
import boto3  # pip install boto3
from botocore.client import Config
from dotenv import load_dotenv

import ae_file_util
import ae_util
from .ae_logger import ae_log

cur_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(cur_dir, '..', '.env'), encoding='utf-8')

LOCAL_ROOT = os.path.join(cur_dir, '..')

class AWS_CONST:
    BASE_BUCKET_NAME = os.getenv('S3_BUCKET')
    ROOT_BUCKET_PATH = ''
    CACHE_DIR = 'cache_data'
    EBEST_DIR = 'ebest_theme'
    EBEST_CACHE_DIR = CACHE_DIR + '/' + EBEST_DIR
    REGION = "ap-northeast-2"
    KEYID = os.getenv('AWS_ACCESS_KEY_ID')
    ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    TIME_ZONE = "KR"

    TEMP_DIR = os.getenv('TEMP_DIR')
    # TEMP_PATH = os.path.join(cur_dir, '..', TEMP_DIR)
    # if not os.path.isdir(TEMP_PATH):
    #     os.mkdir(TEMP_PATH)

class AWS_S3:
    _instance = None
    isDownloading = False
    isUploading = False
    isProgress = False
    fnProgress = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)

        return class_._instance

    def __init__(self):
        self.AWS_CONST = AWS_CONST()

        self.awsSession = self.createSession()
        self.setTimeZone()

    # for sync aws current(RPI) to server
    def setTimeZone(self):
        pass
        # if self.AWS_CONST.TIME_ZONE == "KR":
        #     os.system('timedatectl Asia/Seoul')

    def createSession(self):
        session = boto3.Session(
            aws_access_key_id=self.AWS_CONST.KEYID,
            aws_secret_access_key=self.AWS_CONST.ACCESS_KEY,
            region_name=self.AWS_CONST.REGION
        )
        return session

    def uploadfile(self, srcPath, destBucket, destFileName='', progress=True):
        session = self.awsSession
        config = Config(connect_timeout=10, read_timeout=10)
        s3_connect = session.resource('s3', config=config)
        self.isProgress = progress
        try:
            if destFileName == '':
                splitChar = '/'
                strSplit = srcPath.split(splitChar)
                if ae_util.str_len(strSplit) > 0:
                    destFileName = strSplit[ae_util.str_len(strSplit) - 1]
            dstPath = destBucket + '/' + destFileName
            s3_connect.meta.client.upload_file(srcPath, self.AWS_CONST.BASE_BUCKET_NAME, dstPath, Callback=UploadProgress(srcPath))
            return True
        except Exception as e:
            ae_log.exception(e)
    
    def get_bucket(self):
        session = self.awsSession
        config = Config(connect_timeout=10, read_timeout=10)
        s3_connect = session.resource('s3', config=config)
        bucket = s3_connect.Bucket(self.AWS_CONST.BASE_BUCKET_NAME)
        return bucket

    def downloadfile(self, src_path, dst_path, progress=True):
        session = self.awsSession
        config = Config(connect_timeout=10, read_timeout=10)
        s3_connect = session.resource('s3', config=config)
        try:
            if type(src_path) is str:
                src_path = src_path.split()
            # without duplicate
            src_path = list(set(src_path))
            for download_file in src_path:
                filename = os.path.basename(download_file)
                if self.AWS_CONST.BASE_BUCKET_NAME in download_file:
                    download_file = download_file.replace(self.AWS_CONST.BASE_BUCKET_NAME + '/', '')
                temp_dst_path = dst_path
                if temp_dst_path is None or temp_dst_path == '':
                    temp_dst_path = os.path.join(AWS_CONST.TEMP_PATH, filename)
                elif os.path.isdir(temp_dst_path):
                    temp_dst_path = os.path.join(temp_dst_path, filename)
                if os.path.exists(temp_dst_path):
                    ae_file_util.delete_file(temp_dst_path)

                filesize = 0
                bucket = s3_connect.Bucket(self.AWS_CONST.BASE_BUCKET_NAME)
                for o in bucket.objects.all():
                    if filename in o.key:
                        filesize = o.size
                        break
                self.isProgress = progress
                if self.AWS_CONST.ROOT_BUCKET_PATH in download_file:
                    bucketPath = download_file
                else:
                    bucketPath = self.AWS_CONST.ROOT_BUCKET_PATH + download_file
                ae_log.debug("aws download file:%s, dst:%s(%s)" % (bucketPath, temp_dst_path, ae_file_util.sizeof_fmt(filesize)))
                bucket.download_file(bucketPath, temp_dst_path, Callback=DownloadProgress(filesize))
            return True
        except Exception as e:
            ae_log.error(e)
            return False

    def get_all_file_list(self):
        file_list = []
        try:
            session = self.awsSession
            config = Config(connect_timeout=10, read_timeout=10)
            s3_connect = session.resource('s3', config=config)
            bucket = s3_connect.Bucket(self.AWS_CONST.BASE_BUCKET_NAME)
            for o in bucket.objects.all():
                file_list.append(o)
        except Exception as e:
            ae_log.exception(e)
        finally:
            return file_list

    def download_all(self, dest_path:str, exclude_dir:[], skip_exist: bool = False):
        all_list = self.get_all_file_list()

        for bucket_file in all_list:
            src_path = bucket_file.key
            arr_tmp = src_path.split('/')
            if arr_tmp[0] in exclude_dir:
                continue
            loca_dir_full = dest_path
            for name in arr_tmp:
                if len(name) > 0 and '.' not in name:
                    # dir
                    loca_dir_full = os.path.join(loca_dir_full, name)
                    if not os.path.isdir(loca_dir_full):
                        os.mkdir(loca_dir_full)
                else:
                    if len(name) == 0:
                        continue
                    # file
                    local_path = os.path.join(loca_dir_full, name)
                    if os.path.exists(local_path):
                        if skip_exist:
                            continue
                        else:
                            os.remove(local_path)

                    self.downloadfile(bucket_file.key, local_path)

    def get_df_from_corr_s3(self, date_ref, Ndays):
        ''''''
        data_key = f'corr-deepgraph/{date_ref[:4]}/{date_ref[4:6]}/{date_ref[6:8]}/corr_{date_ref}_N{Ndays}.csv'
        corr_obj = self.get_bucket().Object(
                key=data_key)
        csv = io.BytesIO(corr_obj.get()['Body'].read())
        df = pd.read_csv(csv, index_col=0, dtype={'s':str,'t':str})
        return df

class DownloadProgress(object):
    def __init__(self, filesize):
        self._seen_so_far = 0
        self.filesize = filesize
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            if AWSManager.isProgress:
                ae_log.debug(f'down from aws {self._seen_so_far} / {self.filesize}')


# for upload progress
class UploadProgress(object):
    def __init__(self, filePath):
        self.filepath = filePath
        self._seen_so_far = 0
        statinfo = os.stat(filePath)
        self.filesize = statinfo.st_size
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            if AWSManager.isProgress:
                ae_log.debug(f'{self.filepath} {self._seen_so_far} / {self.filesize}')

AWSManager = AWS_S3()

if __name__ == '__main__':
    # test
    ae_log.debug('AWS S3 TEST')
    df = AWSManager.get_df_from_corr_s3('20200619', 10)
    print(df.shape)
    # Upload
    # AWSManager.uploadfile('./../db.sqlite3', 'cache_data')

    # get all file list
    # file_list = AWSManager.get_all_file_list()
    # ae_log.debug('file_list',file_list)

    # down file list

    # AWSManager.download_all(LOCAL_ROOT, [], skip_exist=False)