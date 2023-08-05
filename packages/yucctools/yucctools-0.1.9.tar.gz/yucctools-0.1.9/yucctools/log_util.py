"""
记录日志
"""

import os
import logging
import datetime


def logger(filepath=None):
    """
    生成logger实例
    :return: logger实例
    """
    # 生成日志路径
    # 1. 如果为文件夹，则返回文件夹下的路径名称
    # 2. 如果为文件，则直接使用
    # 3. 如果为空、非文件、非文件夹、文件夹或文件不存在等其他情况，则不写日志入文件
    # 一并返回绝对路径
    # 文件夹：相对路径或绝对路径的文件夹,下面生成文件
    if filepath and os.path.isdir(filepath):
        log_file = os.path.join(filepath, f"{datetime.datetime.now().strftime('%Y-%m-%d.%H-%M-%S')}.log")
        abs_log_file = os.path.asbpath(log_file)
    # 文件：相对或绝对路径
    elif filepath:
        # 得到文件的绝对路径
        try:
            abs_log_file = os.path.abspath(filepath)
        except:
            # 其他情况, 不写入文件
            abs_log_file = None
    # 其他情况：默认是空
    else:
        abs_log_file = None

    # create logger with a name
    logger = logging.getLogger()
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
                '%(asctime)s %(filename)s:%(lineno)5s %(funcName)20s() %(levelname)-8s %(message)s',
                datefmt="%m/%d/%Y %H:%M:%S")
        # 是否写入文件
        if abs_log_file:
            # create file handler which logs even debug messages
            fh = logging.FileHandler(abs_log_file, encoding='utf-8')
            fh.setLevel(10)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        # 写入控制台
        ch = logging.StreamHandler()
        ch.setLevel(10)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # 第一条日志，记录日志文件所在位置
    logger.info(f'log file: {abs_log_file}')
    return logger
