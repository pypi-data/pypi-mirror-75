# -*- coding:utf-8 -*-
# Author:lixuecheng
from requestQ.package.domssql import DoMssql
from requestQ.package.domysql import DoMysql
from requestQ.package.dorequest import DoRequest
import os
import re
import json
from requestQ.package.logger import logger
from requestQ.package.report import TestReport

config_dict = {'dbs': {}, 'report': {'is_print': True,
                                     'html': None, 'name': '', 'info': []}, 'headers': {}, 'id': 0}
global_dict = {}
report = TestReport()


def add_sqlserver(name: str, ip: str, user: str, password: str, dbname: str, port=1433, is_autocommit=False):
    db = DoMssql(ip, user, password, dbname, port, is_autocommit)  # 报错就报错了
    if name in config_dict['dbs']:
        raise Exception('指定数据库名称已存在')
    else:
        config_dict['dbs'][name] = db


def add_mysql(name: str, ip: str, user: str, password: str, dbname: str, port=1433, is_autocommit=False):
    db = DoMysql(ip, user, password, dbname, port, is_autocommit)  # 报错就报错了
    if name in config_dict['dbs']:
        raise Exception('指定数据库名称已存在')
    else:
        config_dict['dbs'][name] = db


def add_headers(headers: dict):
    if isinstance(headers, dict):
        config_dict['headers'].update(headers)
    else:
        raise Exception('导入的请求头格式不正确')


def get_id():
    config_dict['id'] += 1
    return 't'+str(config_dict['id'])


def set_print(is_print=True):
    config_dict['report']['is_print'] = is_print


def save_report(report_path, testName=None):
    config_dict['report']['html'] = report_path
    config_dict['report']['name'] = testName
    _make_report()



def add_globals(k_v: dict):
    global_dict.update(k_v)


def if_print(v):
    if config_dict['report']['is_print']:
        print(v)


def test(name: str,  *expect_types, **kwargs):
    '''
    :param name str 必填，整个测试场景的名称
    :param expect_type expect 必填，单挑执行、检验




    '''
    err = ''
    run_record = {'label': name, 'status': '未运行', 'children': [], 'msg': ''}
    local_dict = global_dict.copy()  # 设置本地缓存
    if_print(f'用例{name}开始执行：')
    # # 运行起始操作
    # if "setUp" in kwargs and kwargs['setUp'] is not None:
    #     try:
    #         kwargs['setUp'](local_dict)
    #         print('\tok\t初始化执行成功')
    #     except Exception as e:

    #         run_record['status'] = 0
    #         run_record['msg'] = '预置条件运行失败：'+str(e)
    #         if config_dict['report']['is_print']:
    #             print('\terr\t初始化执行失败')
    #         config_dict['report']['info'].append(run_record)
    #         return None
    # # 创建请求对象
    req = DoRequest()
    # 添加统一请求头
    req.add_session_headers(config_dict['headers'])
    # 检验是否可以运行
    for expect_type in expect_types:
        if err != '':
            run_record['record'].append(
                {'id':get_id(),'url': expect_type.get_url(local_dict), 'status': '未运行', 'msg': '前置用例报错，当前无法执行','time':''})
            if config_dict['report']['is_print']:
                print('\tskip\t'+expect_type.get_url(local_dict))

            continue
        if isinstance(expect_type, _checkRes) and expect_type.get_status:

            expect_type._run(req, local_dict)

            if not expect_type.res_status:
                run_record['record'].append(
                    {'url': expect_type.url, 'status': 2, 'msg': f'请求失败，错误代码：{expect_type.err_code},错误原因：{expect_type.e}'})
                err = f'请求失败，错误代码：{expect_type.err_code},错误原因：{expect_type.e}'
                run_record['status'] = 2
                if config_dict['report']['is_print']:
                    print('\terr\t'+expect_type.url+err)

                # print(expect_type.e)
                # print(expect_type.err_code)
            else:
                expect_type._runOrder()
                if not expect_type.res_status:
                    run_record['record'].append(
                        {'url': expect_type.url, 'status': 2, 'msg': f'结果校验错误，错误代码：{expect_type.err_code},错误原因：{expect_type.e}'})
                    err = f'结果校验错误，错误代码：{expect_type.err_code},错误原因：{expect_type.e}'
                    run_record['status'] = 2
                    if config_dict['report']['is_print']:
                        print('\terr\t'+expect_type.url+err)
                else:
                    run_record['record'].append(
                        {'url': expect_type.url, 'status': 1, 'msg': f'运行正确'})
                    if config_dict['report']['is_print']:
                        print('\tok\t'+expect_type.url+",运行成功")
                    run_record['status'] = 1
        else:
            run_record['record'].append(
                {'url': expect_type.url, 'status': 0, 'msg': f'代码编写错误，错误原因：,expect_type参数填写格式错误或者没有添加校验信息'})
            err = expect_type.url+',expect_type参数填写格式错误或者没有添加校验信息'
            run_record['status'] = 2
            if config_dict['report']['is_print']:
                print('\terr\t'+expect_type.url+err)

    try:
        if tearDown is not None:
            # TODO 还没写
            tearDown(local_dict, expect_type._get_res())
    except:
        pass
    config_dict['report']['info'].append(run_record)


def _make_report():
    for i in config_dict['dbs']:
        config_dict['dbs'][i].close()

    report.set_report_name(config_dict['report']['name'])
    for i in config_dict['report']['info']:
        # {'name': name, 'status': 0, 'record': [], 'msg': ''}
        report.add_res(i['name'], i['status'], i['msg'])
        for j in i['record']:
            report.add_res(j['url'], j['status'], j['msg'])
    report.create_report(config_dict['report']['html'])


def expect(method: str, url: str, data=None, headers=None, files=None, file_name=None, proxies=None):
    req_info = {}
    req_info['method'] = method.upper()
    req_info['url'] = url
    req_info['data'] = data
    req_info['headers'] = headers
    req_info['files'] = files
    req_info['file_name'] = file_name
    req_info['proxies'] = proxies
    return _getRes(req_info)


def test_match(res, val):
    '''
    测试正则提取的正确性
    '''
    pass


def setUp(*sqls):
    '''
    sqls dict {'sqlName':'','sql':'','save':'可不填',name:'可不填'}
    '''
    def tmp(local_dict):
        dbs = set()
        for i in sqls:
            if i['sqlName'] in config_dict['dbs']:
                config_dict['dbs'][i['sqlName']].run(i['sql'])
                if not config_dict['dbs'][i['sqlName']].status:
                    for x in dbs:
                        x.rollback()
                    raise Exception(config_dict['dbs'][i['sqlName']].e)
                if 'save' in i and i['save'] and 'name' in i and i['name']:
                    if len(config_dict['dbs'][i['sqlName']].res) > 0:
                        res = config_dict['dbs'][i['sqlName']].res[0]
                        if i['name'] in res:
                            local_dict[i['save']] = str(res[i['name']])
                        else:
                            raise Exception(
                                i['save']+'保存值失败，{}字段不在结果中'.format(str(i['name'])))

                    else:
                        raise Exception(i['sql']+'没有运行结果，无法提取值保存')
            else:
                for x in dbs:
                    x.rollback()
                raise Exception(i['sqlName']+',未设置该数据库名称')
        for x in dbs:
            x.commit()

    return tmp


class _getRes:

    def __init__(self, req_info):
        self.req_info = req_info

    def get(self, get_function: str):
        return _checkRes(get_function, self.req_info)

    def getAll(self):
        return _checkRes(None, self.req_info)


class _checkRes:
    def __init__(self, get_function, req_info):

        self.req_info = req_info

        self.res = None
        self.res_type = None
        self.res_status = False
        self.get_status = False
        self.e = '未运行'
        self._run_order = [{'type': 0, 'val': str(get_function)}]
        self.val = None
        self.val_type = None
        self.req_val = None
        self.res_val = None
        self.is_no = False
        self.err_code = 0
        self.url = ''

    def equal(self, val):
        self._run_order.append({'type': 1, 'val': val})
        self.get_status = True
        return self

    def has(self, val):
        self._run_order.append({'type': 2, 'val': val})
        self.get_status = True
        return self

    def save(self, name):
        self._run_order.append({'type': 3, 'val': name})

        return self

    def save_g(self, name):
        self._run_order.append({'type': 7, 'val': name})

        return self

    def save_headers(self, header_name, name):
        self._run_order.append({'type': 8, 'val': name, 'get': header_name})

    def match(self, regType):
        self._run_order.append({'type': 4, 'val': str(regType)})
        self.get_status = True
        return self

    def decrypt(self, func):
        self.val, self.res_type = func(self.val)

    def no(self):

        self._run_order.append({'type': 5})
        return self

    def lenSql(self, sqlname, sql, expect_len=1):
        self._run_order.append(
            {'type': 6, 'sqlname': sqlname, 'sql': sql, 'len': expect_len})
        self.get_status = True
        return self

    def get(self, get_function):

        self._run_order.append({'type': 0, 'val': str(get_function)})
        return self

    def getAll(self):

        self._run_order.append({'type': 0, 'val': None})
        return self

    def get_url(self, local_dict):
        self.url = self.req_info['url']
        v1 = re.findall(r"\$\{(.+?)\}", self.url)

        for i in v1:
            if i in local_dict:

                self.url = self.url.replace('${'+i+'}', local_dict[i])

            else:
                logger.warning(f"参数{i}无法获取")
        return self.url

    def _run(self, req, local_dict):
        self.local_dict = local_dict

        try:
            req_info = {}
            self.url = self.req_info['url']
            for k, v in self.req_info.items():
                is_json = False
                if not isinstance(v, str):
                    try:
                        v = json.dumps(v, ensure_ascii=False)
                        is_json = True
                    except Exception as e:
                        self.err_code = 1001
                        self.e = str(e)
                        self.res_status = False
                        return None
                v1 = re.findall(r"\$\{(.+?)\}", v)

                for i in v1:
                    if i in local_dict:

                        v = v.replace('${'+i+'}', local_dict[i])

                    else:
                        logger.warning(f"参数{i}无法获取")
                if is_json:
                    try:
                        v = json.loads(v)
                    except Exception as e:
                        self.err_code = 1002
                        self.e = str(e)
                        self.res_status = False
                        return None

                req_info[k] = v
            self.url = req_info['url']
            self.res = req.run(**req_info)
            self.req_val = req.req

            if req.status:
                self.res_val = req.res
                self.res_status = True
                self.e = ''
            else:
                self.err_code = 1003
                self.res_status = False
                self.e = req.e
        except Exception as e:
            self.err_code = 1004
            self.e = str(e)
            self.res_status = False

    def _getRes(self):
        return self.res

    def _runOrder(self):

        for i in self._run_order:

            if self.res_status:
                if i['type'] == 0:
                    self.is_no = False
                    self._get_val(i['val'])
                    logger.info('提取值：'+str(self.val))
                elif i['type'] == 1:

                    logger.info(f'期望值：{i["val"]},结果值：{self.val}')
                    if str(i['val']).lower() != str(self.val).lower() and not self.is_no:
                        self.e = f'期望相同，比较失败，期望值：{str(i["val"]).lower()},结果值：{str(self.val).lower()}'
                        self.res_status = False
                        self.err_code = 1005
                    elif self.is_no and str(i['val']).lower() == str(self.val).lower():
                        self.e = f'期望不同，比较失败，期望值：{str(i["val"]).lower()},结果值：{str(self.val).lower()}'
                        self.res_status = False
                        self.err_code = 1006
                    self.is_no = False
                elif i['type'] == 2:

                    logger.info(f'期望含有值：{i["val"]},结果值：{self.val}')
                    if str(i['val']) not in str(self.val) and not self.is_no:
                        self.e = f'期望含有，取值失败，期望含有值：{i["val"]},结果值：{self.val}'
                        self.res_status = False
                        self.err_code = 1007
                    elif str(i['val']) in str(self.val) and self.is_no:
                        self.e = f'期望不含有，取到值，期望含有值：{i["val"]},结果值：{self.val}'
                        self.res_status = False
                        self.err_code = 1008
                    self.is_no = False

                elif i['type'] == 3:
                    self.local_dict[str(i['val'])] = self.val
                    logger.info(f"{str(i['val'])}保存值{str(self.val)}")
                elif i['type'] == 4:
                    logger.info(f'期望匹配值：{i["val"]},结果值：{self.val}')
                    tmp = re.findall(str(i['val']), str(self.val))
                    if len(tmp) == 0 and not self.is_no:
                        self.e = f'期望无法匹配，期望匹配值：{i["val"]},结果值：{self.val}'
                        self.res_status = False
                        self.err_code = 1009
                    elif len(tmp) != 0 and self.is_no:
                        self.e = f'期望无匹配，期望匹配值：{i["val"]},结果值：{self.val}'
                        self.res_status = False
                        self.err_code = 1010

                elif i['type'] == 5:
                    self.is_no = not self.is_no
                elif i['type'] == 6:

                    self._run_sql(i['sqlname'], i['sql'], i['len'])
                    self.is_no = False
                elif i['type'] == 7:
                    self.local_dict[str(i['val'])] = self.val
                    global_dict[str(i['val'])] = self.val
                    logger.info(f"{str(i['val'])}保存公共值{str(self.val)}")
                elif i['type'] == 8:
                    if str(i['header_name']) in self.res_val['headers']:
                        self.local_dict[str(i['val'])] = self.res_val['headers'][str(
                            i['header_name'])]
                        global_dict[str(i['val'])] = self.res_val['headers'][str(
                            i['header_name'])]
                        logger.info(
                            f"{str(i['val'])}保存公共值{str(self.res_val['headers'][str(i['header_name'])])}")

                    else:
                        self.e = f'保存值失败：请求头{i["header_name"]}不在请求头中' + \
                            str(self.res_val['headers'])
                        self.res_status = False
                        self.err_code = 1011

                else:
                    raise Exception("我是谁，我从哪里来，要到哪里去？")
            else:

                break

    def _get_val(self, val):
        self.res_type = self.res_val['header_type']['type']

        if self.res_type == 'json':
            try:
                # self.val = json.dumps(self.res, ensure_ascii=False)
                self.val = self.res
                if val is None:
                    return None

                for i in val.split('.'):
                    if isinstance(self.val, dict):
                        if str(i) in self.val:

                            self.val = self.val[str(i)]
                        else:
                            self.e = f'提取结果：{val},在{str(i)}错误，请检查，提取值不在结果中'
                            self.res_status = False
                            self.err_code = 1012
                    elif isinstance(self.val, list):
                        try:
                            i = int(i)
                        except:
                            self.e = f'提取结果：{val},在{str(i)}错误，请检查，此处是list，不是对象'
                            self.res_status = False
                            self.err_code = 1013
                        if len(self.val) < i:
                            self.val = self.val[i]
                        else:
                            self.e = f'提取结果：{val},在{str(i)}错误，请检查,提取的值大于结果的值'
                            self.res_status = False
                            self.err_code = 1014
                    elif isinstance(self.val, str):
                        self.e = f'提取结果：{val},在{str(i)}错误，请检查,当前结果为字符串无法再提取'
                        self.res_status = False
                        self.err_code = 1015
                    else:
                        self.e = f'提取结果：{val},在{str(i)}错误，请检查,当前结果未知格式{type(self.val)}'
                        self.res_status = False
                        self.err_code = 1016

            except Exception as e:
                self.e = '结果提取错误：'+str(e)
                self.res_status = False
                self.err_code = 1017
        elif self.res_type == 'text':
            self.val = self.res
            if val is None:
                return None

            v = re.findall(val, self.val)
            if len(v) == 0:
                self.e = f'提取结果：{val},错误，请检查,当前未得到提取值'
                self.res_status = False
                self.err_code = 1018
            elif len(v) == 1:
                self.val = v[0]
            else:
                self.e = f'提取结果：{val},错误，请检查,当前有多个提取值'
                self.res_status = False
                self.err_code = 1019
        else:
            self.e = '结果为字节，无法提起'
            self.res_status = False
            self.err_code = 1020

    def _run_sql(self, name, sql, lens):

        if name in config_dict['dbs']:
            try:
                v1 = re.findall(r"\$\{(.+?)\}", sql)
                for i in v1:
                    if i in self.local_dict:
                        sql = sql.replace('${'+i+'}', str(self.local_dict[i]))
                    else:
                        logger.warning(f"参数{i}无法获取")
                logger.info("sql执行："+str(sql))
                config_dict['dbs'][name].run(sql)
                config_dict['dbs'][name].commit()
                res = config_dict['dbs'][name].res
                logger.info("sql执行结果："+str(res))

                l1 = len(res)
                if l1 != lens and not self.is_no:
                    self.e = '结果长度不等于期望长度'
                    self.res_status = False
                    self.err_code = 1021
                elif l1 == lens and self.is_no:
                    self.e = '结果长度等于期望长度'
                    self.res_status = False
                    self.err_code = 1022

            except Exception as e:
                config_dict['dbs'][name].rollback()
                self.e = name+f'数据库执行{sql}出错：'+str(e)
                self.res_status = False
                self.err_code = 1023
        else:
            self.e = '指定数据库未设置：'+name
            self.res_status = False
            self.err_code = 1024
