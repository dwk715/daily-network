# -*- coding:utf-8 -*-
import datetime
import logging
import logging.handlers
import os
import sys


class logmode(object):
    def __init__(self, log_file=None, logger=None):
                
        #创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        #创建一个handler，用于写入日志文件
        self.log_filename = log_file 
        self.log_dir = sys.path[0] + '/log'
        self.log_name = os.path.join(self.log_dir, self.log_filename)

        fh = logging.handlers.TimedRotatingFileHandler(self.log_name, when='D', interval=1, backupCount=0)
        fh.suffix = "%Y-%m-%d.log"
        fh.setLevel(logging.DEBUG)

        #定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(message)s'
        )
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)
        fh.close()

    def getlog(self):
        return self.logger