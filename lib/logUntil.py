# coding=utf-8
import logging
import time
import os
import configinfo as cf


class Log(object):
    def __init__(self):
        self.logFileName = os.path.join(cf.log_path, '{0}.log'.format(time.strftime('%Y%m%d')))

    def __logconsole(self, level, message):
        # 创建一个logger
        logger = logging.getLogger()
        # 设置logger级别
        # 级别高低顺序：NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
        logger.setLevel(logging.DEBUG)
        # 创建一个 handler，用于写入日志文件
        fh = logging.FileHandler(self.logFileName, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s\t-\t%(levelname)s\t-\t%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        # 记录一条日志
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__logconsole('debug', message)

    def info(self, message):
        self.__logconsole('info', message)

    def warning(self, message):
        self.__logconsole('warning', message)

    def error(self, message):
        self.__logconsole('error', message)


if __name__ == '__main__':
    Log().debug('this is debug')
    Log().error('this is error')
    Log().info('this is info')
    Log().error('this is error')
