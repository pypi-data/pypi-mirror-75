# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     log
   Description :
   Author :       艾登科技 Asdil
   date：          2020/7/9
-------------------------------------------------
   Change Activity:
                   2020/7/9:
-------------------------------------------------
"""
__author__ = 'Asdil'
from loguru import logger
import logging


def add(name, level=logging.INFO, log_path=None):
    """add方法用于新建一个log

    Parameters
    ----------
    name : str
        模块名称
    level: logging.INFO
        日志级别
    log_path: str
        保存路径
    Returns
    ----------
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if log_path is not None:
        # create a file handler
        handler = logging.FileHandler(log_path)
        handler.setLevel(level)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    return logger


def example():
    """example方法用于

    Parameters
    ----------
    param : str

    Returns
    ----------
    """
    # logger.add("somefile.log", rotation="1 MB", enqueue=True, level="INFO")  # 异步写入
    return 0
