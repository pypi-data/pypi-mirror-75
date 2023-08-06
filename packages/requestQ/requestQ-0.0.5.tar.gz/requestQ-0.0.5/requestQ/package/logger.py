# -*- coding:utf-8 -*-
# Author:lixuecheng
import logging
import os
import time
import functools


def color_print(*require):
    '''
    格式：[{'type':'no','val':'asas'}]

    type:no  success  warn err  normal
    '''
    ss=''
    for d in require:
        vv=''
        if 'val' in d:
            vv=str(d['val'])
        else:
            vv=' '
        if 'type' in d:
            if d['type']=='success':
                ss+='\033[1;37;42m'
                ss+=vv
                ss+='\033[0m'
            elif d['type']=='warn':
                ss+='\033[1;33m'
                ss+=vv
                ss+='\033[0m'
            elif d['type']=='err':
                ss+='\033[1;35;41m'
                ss+=vv
                ss+='\033[0m'
            elif d['type']=='normal':
                ss+='\033[1;36m'
                ss+=vv
                ss+='\033[0m'
            else:
                ss+=vv
        else:
            ss+=vv
    print(ss)



                

            



class ContextFilter(logging.Filter):
    # filename = 'IP'
    # lineno = 'USER'
    def __init__(self, filename, lineno, funcname):
        self.filename = filename
        self.lineno = lineno
        self.funcname = funcname

    def filter(self, record):
        record.filename = self.filename
        record.lineno = self.lineno
        record.funcName = self.funcname
        return True






# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Log等级总开关
logger.propagate = False

# 第二步，创建一个 file handler，用于写入日志文件
rq = time.strftime('%Y-%m-%d-%p', time.localtime(time.time()))

# all级别的日志输出
log_path = os.getcwd() + '/../Logs/all/'
log_name = log_path + rq + '_all.log'
logfile = log_name
if not os.path.exists(log_path):
    # print(log_path)
    try:
        
        os.makedirs(log_path)
    except :
        
        log_path = os.getcwd() + '/Logs/all/'
        log_name = log_path + rq + '_all.log'
        logfile = log_name
        if not os.path.exists(log_path):
            os.makedirs(log_path)
for root, dirs, files in os.walk(os.path.dirname(log_path)):
    for i in files:
        fpath = os.path.join(root, i)
        if os.path.getsize(fpath) == 0:
            os.remove(fpath)
if not os.path.exists(logfile):
    f = open(logfile, mode='w', encoding="utf-8")
    f.close()
fh_all = logging.FileHandler(logfile, mode='a', encoding='utf-8')
fh_all.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

# debug以上日志handler
# rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.getcwd() + '/../Logs/debug/'
log_name = log_path + rq + '_debug.log'
logfile = log_name
if not os.path.exists(log_path):
    try:
        os.makedirs(log_path)
    except :
        log_path = os.getcwd() + '/Logs/debug/'
        log_name = log_path + rq + '_debug.log'
        logfile = log_name
        if not os.path.exists(log_path):
            os.makedirs(log_path)
for root, dirs, files in os.walk(os.path.dirname(log_path)):
    for i in files:
        fpath = os.path.join(root, i)
        if os.path.getsize(fpath) == 0:
            os.remove(fpath)
if not os.path.exists(logfile):
    f = open(logfile, mode='w', encoding="utf-8")
    f.close()
fh_debug = logging.FileHandler(logfile, mode='a', encoding='utf-8')
fh_debug.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
debug_filter = logging.Filter()
debug_filter.filter = lambda record: record.levelno == fh_debug.level
fh_debug.addFilter(debug_filter)

# info以上日志handler
# rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.getcwd() + '/../Logs/info/'
log_name = log_path + rq + '_ifo.log'
logfile = log_name

if not os.path.exists(log_path):
    try:
        os.makedirs(log_path)
    except :
        log_path = os.getcwd() + '/Logs/info/'
        log_name = log_path + rq + '_ifo.log'
        logfile = log_name
        if not os.path.exists(log_path):
            os.makedirs(log_path)
for root, dirs, files in os.walk(os.path.dirname(log_path)):
    for i in files:
        fpath = os.path.join(root, i)
        if os.path.getsize(fpath) == 0:
            os.remove(fpath)
if not os.path.exists(logfile):
    f = open(logfile, mode='w', encoding="utf-8")
    f.close()
fh_info = logging.FileHandler(logfile, mode='a', encoding='utf-8')
fh_info.setLevel(logging.INFO)  # 输出到file的log等级的开关
info_filter = logging.Filter()
info_filter.filter = lambda record: record.levelno == fh_info.level
fh_info.addFilter(info_filter)

# warn以上日志handler
# rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.getcwd() + '/../Logs/warn/'
log_name = log_path + rq + '_warn.log'
logfile = log_name

if not os.path.exists(log_path):
    try:
        os.makedirs(log_path)
    except :
        log_path = os.getcwd() + '/Logs/warn/'
        log_name = log_path + rq + '_warn.log'
        logfile = log_name
        if not os.path.exists(log_path):
            os.makedirs(log_path)
for root, dirs, files in os.walk(os.path.dirname(log_path)):
    for i in files:
        fpath = os.path.join(root, i)
        if os.path.getsize(fpath) == 0:
            os.remove(fpath)
if not os.path.exists(logfile):
    f = open(logfile, mode='w', encoding="utf-8")
    f.close()
fh_warn = logging.FileHandler(logfile, mode='a', encoding='utf-8')
fh_warn.setLevel(logging.WARNING)  # 输出到file的log等级的开关
warn_filter = logging.Filter()
warn_filter.filter = lambda record: record.levelno == fh_warn.level
fh_warn.addFilter(warn_filter)

# warn以上日志handler
log_path = os.getcwd() + '/../Logs/error/'
log_name = log_path + rq + '_error.log'
logfile = log_name
if not os.path.exists(log_path):
    try:
        os.makedirs(log_path)
    except :
        log_path = os.getcwd() + '/Logs/error/'
        log_name = log_path + rq + '_error.log'
        logfile = log_name
        if not os.path.exists(log_path):
            os.makedirs(log_path)
for root, dirs, files in os.walk(os.path.dirname(log_path)):
    for i in files:
        fpath = os.path.join(root, i)
        if os.path.getsize(fpath) == 0:
            os.remove(fpath)
if not os.path.exists(logfile):
    f = open(logfile, mode='w', encoding="utf-8")
    f.close()
fh_error = logging.FileHandler(logfile, mode='a', encoding='utf-8')
fh_error.setLevel(logging.ERROR)  # 输出到file的log等级的开关
error_filter = logging.Filter()
error_filter.filter = lambda record: record.levelno == fh_error.level
fh_error.addFilter(error_filter)

# 控制台 handler
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)  # 控制台输出的日志级别

# 第三步，定义handler的输出格式
formatter1 = logging.Formatter(
    "%(asctime)s - %(message)s")
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d](%(funcName)s) - %(levelname)s: %(message)s")
fh_debug.setFormatter(formatter)
fh_info.setFormatter(formatter)
fh_warn.setFormatter(formatter)

fh_error.setFormatter(formatter)
ch.setFormatter(formatter1)
fh_all.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh_debug)
logger.addHandler(fh_info)
logger.addHandler(fh_warn)
logger.addHandler(fh_error)
logger.addHandler(fh_all)

logger.addHandler(ch)


# print(logger.name)


# ------------------------日志配置信息-----------------end

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        dicc = {}
        dinp = {}
        varnames = func.__code__.co_varnames
        deft = func.__defaults__
        if deft is None:
            deft = ()

        for i in range(len(args)):
            dinp[varnames[i]] = str(args[i])
        for j in range(len(deft)):
            try:
                dinp[varnames[i + j + 1]] = str(deft[j])
            except:
                pass
        for i, j in kw.items():
            dinp[i] = str(j)
        # print(str(func.__name__))
        filter = ContextFilter(
            os.path.basename(str(func.__code__.co_filename)), int(func.__code__.co_firstlineno), str(func.__name__))

        try:
            aa = func(*args, **kw)
        except Exception as e:
            aa = 'err:' + str(e)
            if aa is None:
                dretrun = ''
            elif isinstance(aa, str):
                dretrun = aa
            elif isinstance(aa, tuple):
                dretrun = list(aa)
            else:
                dretrun = str(aa)
            # dicc['run_info'] = dinfo
            dicc['run_input'] = dinp
            dicc['run_return'] = dretrun
            logger.addFilter(filter)
            logger.debug(dicc)
            logger.error(func.__name__ + '运行错误：', exc_info=True)
            logger.removeFilter(filter)

            raise e

        if aa is None:
            dretrun = ''
        elif isinstance(aa, str):
            dretrun = aa
        elif isinstance(aa, tuple):
            dretrun = list(aa)
        else:
            dretrun = str(aa)
        # dicc['run_info'] = dinfo
        dicc['run_input'] = dinp
        dicc['run_return'] = dretrun
        logger.addFilter(filter)
        logger.debug(dicc)
        logger.removeFilter(filter)

        return aa

    return wrapper
