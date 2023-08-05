# -*- coding: utf-8 -*-

# Singleton
import enum
import os

from dotenv import load_dotenv


class AE_ENV_TYPE(enum.Enum):
    AE_ENV_ALL = 0
    # AE_ENV_DB = 0
    # AE_ENV_TELEGRAM = 1

class AeEnvManager(object):
    __single = None  # the one, true Singleton

    def __new__(classtype, *args, **kwargs):
        # Check to see if a __single exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __single objects
        if classtype != type(classtype.__single):
            classtype.__single = object.__new__(classtype, *args, **kwargs)
        return classtype.__single

    def __init__(self, name=None):
        self.env = {}
        for type in AE_ENV_TYPE:
            self.env[type] = ""

    @classmethod
    def instance(cls):
        if None == AeEnvManager.__single:
            AeEnvManager.__single = AeEnvManager()
        return AeEnvManager.__single

    def set_env_path(self, env_type: AE_ENV_TYPE, env_path: str):
        if os.path.exists(env_path):
            self.env[env_type] = env_path
            load_dotenv(dotenv_path=env_path, encoding='utf-8')

        else:
            from .ae_logger import ae_log
            ae_log.error(f"{env_type}의 환경 파일이 없습니다. => {env_path}")

    def get_env_path(self, env_type:AE_ENV_TYPE):
        if env_type in self.env:
            return self.env[env_type]

        raise Exception(f'{env_type}이 정의되지 않았습니다.')

ae_env_manager = AeEnvManager.instance()

if __name__ == '__main__':
    ae_env_manager.set_env_path(AE_ENV_TYPE.AE_ENV_ALL, "env_file_path")