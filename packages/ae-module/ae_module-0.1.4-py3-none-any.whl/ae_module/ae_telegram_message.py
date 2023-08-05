# -*- coding: utf-8 -*-
import os
import sys
import traceback
from datetime import datetime

import pytz
import telegram

from .ae_env_manager import AeEnvManager, AE_ENV_TYPE
from .ae_logger import ae_log
from .ae_telegram_constant import TELEGRAM_COMMAND, TELEGRAM_CMD_STX, TELEGRAM_CMD_SPLIT, TELEGRAM_CMD_ETX

class ae_TelegramMessage:
    tz_seoul = pytz.timezone('Asia/Seoul')

    def __init__(self):
        import os
        from dotenv import load_dotenv
        telegram_env_path = AeEnvManager.instance().get_env_path(AE_ENV_TYPE.AE_ENV_ALL)
        if os.path.exists(telegram_env_path):
            load_dotenv(dotenv_path=telegram_env_path, encoding='utf-8')

        self.TELEGRAM_TEST_CHANNEL_NAME = os.getenv('TELEGRAM_TEST_CHANNEL_NAME')
        self.CHAT_ID_AFRICA_ELEPHANT = os.getenv('CHAT_ID_AFRICA_ELEPHANT')
        self.CHAT_ID_AFRICA_ELEPHANT_ERROR = os.getenv('CHAT_ID_AFRICA_ELEPHANT_ERROR')
        self.CHAT_ID_STOCK_NOTI = os.getenv('CHAT_ID_STOCK_NOTI')

        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.TELEGRAM_API_SESSION = os.getenv('TELEGRAM_API_SESSION')
        self.TELEGRAM_API_SESSION_HEROKU = os.getenv('TELEGRAM_API_SESSION_HEROKU')
        self.TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
        self.TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    def __str__(self):
        return f'TELEGRAM_API_ID = {self.TELEGRAM_API_ID}\nTELEGRAM_API_HASH = {self.TELEGRAM_API_HASH}'

    def send_message(self, msg, chat_id="", token=""):
        """
    	Send a mensage to a telegram_collect user specified on chatId
    	chat_id must be a number!
    	"""
        if len(chat_id) == 0:
            chat_id = self.CHAT_ID_AFRICA_ELEPHANT

        if len(token) == 0:
            token = self.TELEGRAM_TOKEN

        bot = telegram.Bot(token=token)
        str_msg = f'{datetime.now(self.tz_seoul).strftime("%Y-%m-%d %H:%M:%S")} | {msg}'
        bot.sendMessage(chat_id=chat_id, text=str_msg)
        ae_log.info(str_msg)

    def send_protocol(self, cmd: TELEGRAM_COMMAND, args:[] = None):
        bot = telegram.Bot(token=self.TELEGRAM_TOKEN)
        str_arg = ""
        arg_len = 0
        if None != args:
            str_arg = ''.join(args)
            arg_len = len(args)
        str_msg = f'{TELEGRAM_CMD_STX}{TELEGRAM_CMD_SPLIT}{cmd.name}{TELEGRAM_CMD_SPLIT}{arg_len}{TELEGRAM_CMD_SPLIT}{str_arg}{TELEGRAM_CMD_SPLIT}{TELEGRAM_CMD_ETX}'
        bot.sendMessage(chat_id=self.CHAT_ID_AFRICA_ELEPHANT, text=str_msg)
        ae_log.info(str_msg)

    def getTracebackStr(self):
        lines = traceback.format_exc().strip().split('\n')
        rl = [lines[-1]]
        lines = lines[1:-1]
        lines.reverse()
        nstr = ''
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('File "'):
                eles = lines[i].strip().split('"')
                basename = os.path.basename(eles[1])
                lastdir = os.path.basename(os.path.dirname(eles[1]))
                eles[1] = '%s/%s' % (lastdir, basename)
                rl.append('^\t%s %s' % (nstr, '"'.join(eles)))
                nstr = ''
            else:
                nstr += line
        return '\n'.join(rl)

    def send_error(self, msg: str):
        bot = telegram.Bot(token=self.TELEGRAM_TOKEN)
        str_msg = f'[ERROR]\n{msg}'
        bot.sendMessage(chat_id=self.CHAT_ID_AFRICA_ELEPHANT_ERROR, text=str_msg)
        ae_log.info(str_msg)

    def send_exception(self, app_name: str):
        bot = telegram.Bot(token=self.TELEGRAM_TOKEN)
        exc_info = sys.exc_info()
        # traceback.print_exception(*exc_info)
        # trace = self.getTracebackStr()
        formatted_lines = traceback.format_exc().splitlines()
        tele_msg = ""
        for line in formatted_lines:
            tele_msg = tele_msg + line + "\n"
            # print(line)
        str_msg = f'[EXCEPTION] | {app_name} \n{tele_msg}'
        # bot.sendMessage(chat_id=CHAT_ID_AFRICA_ELEPHANT_ERROR, text=str_msg)
        ae_log.error(str_msg)

# ae_tele_message = ae_TelegramMessage()