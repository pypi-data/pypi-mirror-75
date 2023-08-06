#    Copyright 2018-2020 LuomingXu
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   Author : Luoming Xu
#   File Name : log.py
#   Repo: https://github.com/LuomingXu/selfusepy


"""
Python log 增强
"""

import logging
from datetime import datetime, timedelta, timezone
from enum import Enum
from logging import handlers
from typing import List

from selfusepy.utils import RootPath


def __UTC_12__(fmt, timestamp):
    return __delta_base__(-12)


def __UTC_11__(fmt, timestamp):
    return __delta_base__(-11)


def __UTC_10__(fmt, timestamp):
    return __delta_base__(-10)


def __UTC_9__(fmt, timestamp):
    return __delta_base__(-9)


def __UTC_8__(fmt, timestamp):
    return __delta_base__(-8)


def __UTC_7__(fmt, timestamp):
    return __delta_base__(-7)


def __UTC_6__(fmt, timestamp):
    return __delta_base__(-6)


def __UTC_5__(fmt, timestamp):
    return __delta_base__(-5)


def __UTC_4__(fmt, timestamp):
    return __delta_base__(-4)


def __UTC_3__(fmt, timestamp):
    return __delta_base__(-3)


def __UTC_2__(fmt, timestamp):
    return __delta_base__(-2)


def __UTC_1__(fmt, timestamp):
    return __delta_base__(-1)


def __UTC__(fmt, timestamp):
    return __delta_base__(0)


def __UTC1__(fmt, timestamp):
    return __delta_base__(1)


def __UTC2__(fmt, timestamp):
    return __delta_base__(2)


def __UTC3__(fmt, timestamp):
    return __delta_base__(3)


def __UTC4__(fmt, timestamp):
    return __delta_base__(4)


def __UTC5__(fmt, timestamp):
    return __delta_base__(5)


def __UTC6__(fmt, timestamp):
    return __delta_base__(6)


def __UTC7__(fmt, timestamp):
    return __delta_base__(7)


def __UTC8__(fmt, timestamp):
    return __delta_base__(8)


def __UTC9__(fmt, timestamp):
    return __delta_base__(9)


def __UTC10__(fmt, timestamp):
    return __delta_base__(10)


def __UTC11__(fmt, timestamp):
    return __delta_base__(11)


def __UTC12__(fmt, timestamp):
    return __delta_base__(12)


def __delta_base__(delta: int):
    return datetime.now(timezone(timedelta(hours = delta))).timetuple()


class LogTimeUTCOffset(Enum):
    """
    UTC_8 -> UTC-08:00
    UTC8  -> UTC+08:00
    """

    UTC_12 = __UTC_12__
    UTC_11 = __UTC_11__
    UTC_10 = __UTC_10__
    UTC_9 = __UTC_9__
    UTC_8 = __UTC_8__
    UTC_7 = __UTC_7__
    UTC_6 = __UTC_6__
    UTC_5 = __UTC_5__
    UTC_4 = __UTC_4__
    UTC_3 = __UTC_3__
    UTC_2 = __UTC_2__
    UTC_1 = __UTC_1__
    UTC = __UTC__
    UTC1 = __UTC1__
    UTC2 = __UTC2__
    UTC3 = __UTC3__
    UTC4 = __UTC4__
    UTC5 = __UTC5__
    UTC6 = __UTC6__
    UTC7 = __UTC7__
    UTC8 = __UTC8__
    UTC9 = __UTC9__
    UTC10 = __UTC10__
    UTC11 = __UTC11__
    UTC12 = __UTC12__


class Logger(object):
    """
    日志类
    usage: log = Logger('error.log').logger OR log = Logger().logger
           log.info('info')
    """

    def __init__(self, filename = None, time_offset: LogTimeUTCOffset = LogTimeUTCOffset.UTC8, when = 'D',
                 backCount = 3,
                 fmt = '%(asctime)s-[%(levelname)8s]-[%(threadName)15s] %(customPathname)50s(%(lineno)d): %(message)s'):
        """
        init
        :param filename: 储存日志的文件, 为None的话就是不储存日志到文件
        :param when: 间隔的时间单位. S秒, M分, H小时, D天, W每星期(interval==0时代表星期一) midnight 每天凌晨
        :param backCount: 备份文件的个数, 如果超过这个个数, 就会自动删除
        :param time_offset: log的时间, 默认为UTC+8
        :param fmt: 日志格式
        """
        logging.Formatter.converter = time_offset
        self.logger = logging.Logger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(logging.DEBUG)  # 设置日志级别为debug, 所有的log都可以打印出来
        sh = logging.StreamHandler()  # 控制台输出
        sh.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addFilter(LoggerFilter())

        if filename is not None:
            """实例化TimedRotatingFileHandler"""
            th = handlers.TimedRotatingFileHandler(filename = filename, when = when, backupCount = backCount,
                                                   encoding = 'utf-8')
            th.setFormatter(format_str)  # 设置文件里写入的格式
            self.logger.addHandler(th)


class LoggerFilter(logging.Filter):

    def _s_len(self, l: List[str]):
        len: int = 0
        for item in l:
            len += item.__len__() + 1
        return len

    def _replace_underline(self, l: List[str]):
        for i, item in enumerate(l):
            l[i] = item.replace('_', '')

    def filter(self, record: logging.LogRecord):
        s = str(record.pathname).replace('\\', '/').replace(RootPath().root_path, '').replace('/', '.')[1:]
        l: List[str] = s.split('.')
        l.pop(l.__len__() - 1)  # 丢弃最后的文件扩展名'py'
        file_name = l.pop(l.__len__() - 1)
        self._replace_underline(l)  # 有些py文件以'_'开头, 需要删去, 才能取首字母
        i: int = 0
        while self._s_len(l) + file_name.__len__() + record.funcName.__len__() > 50:  # 如果超出了长度再进行缩减操作
            if i >= l.__len__():  # 实在太长了缩减不了, 就算了, 需要保证最后的文件名与函数名的完整
                break
            l[i] = l[i][0]
            i += 1

        l.append(file_name)
        l.append(record.funcName)

        record.customPathname = '.'.join('%s' % item for item in l)
        """
        不能在这边直接就修改
        >>>record.pathname = '.'.join('%s' % item for item in l)
        有可能后面的log依赖这个pathname, 那么这个pathname就被修改了, 
        而没有被系统重新赋予正确的pathname
        例如test.log包中的多层级__init__, 就会出现这种问题
        """
        return True
