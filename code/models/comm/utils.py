import json
import logging
from logging.handlers import RotatingFileHandler

class PromptBankLogger:
    def __init__(self, name=None, level=logging.INFO, log_file=None, max_bytes=200*1000*1000, backup_count=7,
            log_format='%(asctime)s %(module)s:%(lineno)d level-%(levelname)-4s %(message)s'):
        self._formatter = logging.Formatter(log_format)

        if log_file is None:
            self._handler = logging.StreamHandler()
            name = 'StreamHandler' if name is None else name
        else:
            self._handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
            name = log_file if name is None else name

        self._handler.setFormatter(self._formatter)
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)

        self._logger.addHandler(self._handler)

    @property
    def logger(self):
        return self._logger


class ParseUtil:
    @staticmethod
    def get_all_lines(file_path):
        ret = []
        f = None
        try:
            f = open(file_path, encoding='utf-8')
            ret = f.readlines()
        except Exception as e:
            print("[GET ALL LINES ERROR]", e)
        finally:
            if f is not None:
                f.close()
        return ret

    @staticmethod
    def parse_json_file(json_file):
        with open(json_file, encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def parse_jsonl_file(jsonl_file):
        f = open(jsonl_file, "r", encoding='utf-8')
        return [json.loads(line) for line in f]

    @staticmethod
    def parse_log_level(level:str):
        level = level.lower()
        if level == 'debug':
            return logging.DEBUG
        if level == 'info':
            return logging.INFO
        if level == 'warning':
            return logging.WARNING
        if level == 'fatal':
            return logging.FATAL
        if level == 'critical':
            return logging.CRITICAL
        return logging.INFO

    @staticmethod
    def safe_get_float(s, default = 0):
        try:
            return float(s)
        except:
            return default