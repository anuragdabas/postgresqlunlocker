import psycopg2
from psycopg2.extras import DictCursor
from . import consts
import logging
import os
from datetime import datetime

class TimeScale:
    
    @staticmethod
    def get_connection(dbname):
        conn=psycopg2.connect(consts.TimeScale.CONNECTION.value+dbname)
        return conn


    @staticmethod
    def get_cursor(connection):
        return connection.cursor(cursor_factory=DictCursor)


    @staticmethod
    def close(connection):
        try:
            connection.cursor.close()
            connection.close()
            del connection
            return True
        except Exception as e:
            return False

class Logger:
    
    def __init__(self,name,level="info"):
        self.name=name
        self.level=level
        self.level=self._map_level()
        self.format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
        self.formatter=logging.Formatter(self.format,datefmt='%Y-%m-%d %H:%M:%S')
        self.logger=logging.getLogger(self.name)
        self.logger.setLevel(self.level)

    def _map_level(self):
        levels={
        "info":logging.INFO,
        "debug":logging.DEBUG,
        "warning":logging.WARNING,
        "error":logging.ERROR,
        "critical":logging.CRITICAL
                }
        return levels[self.level.lower()]


    @classmethod
    def Logger(cls,name,addHandlers,level="info"):
        logger=cls(name,level)
        if bool(addHandlers):
            logger.add_stream_handler()
            logger.add_file_handler()
        return logger.logger

    def add_stream_handler(self):
        sh=logging.StreamHandler()
        sh.setFormatter(self.formatter)
        sh.setLevel(self.level)
        self.logger.addHandler(sh)

    def add_file_handler(self):
        logpath=consts.Path.LOG_PATH.value
        if not os.path.exists(os.path.join(os.getcwd(),logpath)):
            os.makedirs(logpath)
        logfile=f"{datetime.strftime(datetime.now(),'%Y-%h-%d %H%M%S')}.log"
        fh = logging.FileHandler(filename=os.path.join(logpath,logfile),mode="w",encoding='utf-8')
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

