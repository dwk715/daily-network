#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date: 2018/11/5
# Author :  zlw zly
import datetime
import logging
import logging.handlers
import os
import sys


class logmode(object):
    '''
    log_file: log目录
    logger： log实例
    log级别： info
    '''

    def __init__(self, log_file=None, logger=None):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        self.log_filename = log_file
        self.log_dir = sys.path[0] + '/log'
        self.log_name = os.path.join(self.log_dir, self.log_filename)

        fh = logging.handlers.TimedRotatingFileHandler(
            self.log_name, when='D', interval=1, backupCount=0)
        # fh.suffix = datetime.datetime.now().strftime('-%Y-%m-%d') + '.log'
        fh.suffix = "%Y-%m-%d.log"
        fh.setLevel(logging.INFO)
        '''
        #再创建一个handler，用于stdout
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        '''
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        fh.setFormatter(formatter)
        # sh.setFormatter(formatter)
        self.logger.addHandler(fh)
        # self.logger.addHandler(sh)
        fh.close()
        # sh.close()


# 实例化一个log
log_instance = logmode('daily-network').logger
