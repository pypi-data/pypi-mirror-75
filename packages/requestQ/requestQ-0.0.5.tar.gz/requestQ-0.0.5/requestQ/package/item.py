# -*- coding:utf-8 -*-
# Author:lixuecheng
import uuid
import json
from requestQ.config.sys_config import prioritys
from requestQ.package.baseClass import baseClass
import time
import re
from requestQ.package.logger import logger
import sys




class item:
    def __init__(self, name: str,  data: dict, des='', func: str = 'http', priority='中', hook=None):
        self.label = name
        self.des = des
        self.priority = priority or '中'
        self.func = func
        self.data = data
        self.data_pre = None
        self.msg = ''
        self.status = '未运行'
        self.start_time = 0
        self.end_time = 0
        self.id = uuid.uuid4().hex
        self.time = 0  # 耗时
        self.self_status = True
        if self.priority not in prioritys:
            logger.warning('priority 参数，请输入：'+str(prioritys) +
                           ',当前为：'+self.priority)
            self.priority = '中'

        self.req = None  # 操作数据
        self.res = None  # 结果数据
        self.result_catch = hook  # 结果处理方法
        self.func_instance = None   # 方式实例
        self.local = {}
        self.params = {}
        self.catch_log = []  # 将运行日志
        self.run_log = []  # 运行日志
        self.is_run = False
        self.globals = {}
        self.my_dict = {}  # 结合local和 globals的值
        self.reqf = None
        self.resf = None
        self.is_print = True

    def __str__(self) -> str:
        return json.dumps(self.val_dict(), ensure_ascii=False)

    @staticmethod
    def help():
        print('还没写')

    def print_log(self):
        if self.is_print:
            if self.is_run:
                print('-'*15, '运行结果', '-'*15)
                print(self.val_dict())
                print()
                print('-'*15, '运行步骤结果', '-'*15)
                print(self.run_log)
                print()
                print('-'*15, '请求数据', '-'*15)
                print(self.req)
                print()
                print('-'*15, '响应数据', '-'*15)
                print(self.res)
                print()
                print('-'*15, '环境值（私有）', '-'*15)
                print(self.local)
                print()
                print('-'*15, '环境值（公共）', '-'*15)
                print(self.globals)
                print()
                print('-'*15, '参数使用', '-'*15)
                print(self.params)
                print('-'*15, '结束', '-'*15)
            else:
                self.catch_log.append({'method': 'log', 'status': True})
        return self

    def do_req(self, f):
        '''
        运行方法：输入值为req,lcoal,gloabls,输出同样也是。例子：def(req,mylocal,myglobals) -> req,mylocal,myglobals
        '''

        if not self.is_run:
            self.reqf = f
            return self
        else:
            logger.warning("do_req方法已运行完毕，请再运行前添加")

    def do_res(self, f):
        '''
        运行方法：输入值为res,lcoal,gloabls,输出同样也是。例子：def(res,mylocal,myglobals) -> res,mylocal,myglobals
        '''
        if not self.is_run:
            self.resf = f
            return self
        else:
            logger.warning("do_res方法已运行完毕，请再运行前添加")

    def val_dict(self) -> dict:
        '''
        显示方法的必要属性的内容
        '''
        st = int(self.start_time*1000)
        end = int(self.end_time*1000)
        times = end-st
        return {'id': self.id, 'label': self.label, 'des': self.des, 'priority': self.priority, 'func': self.func,  'msg': self.msg, 'status': self.status, 'start_time': st, 'end_time': end, 'time': times}

    def _add_catch_log(self, ss: dict):
        '''
        把校验的结果整理在一起的方法，外部不调用
        '''
        if self.is_run:
            if self.status == '成功' and self.self_status:
                if ss['status']:

                    self.run_log.append(self._local_catch(ss))
                else:
                    self.self_status = False
                    self.status = '失败'
                    self.msg = ss['msg']
                    self.run_log.append(
                        {'status': '失败', 'msg': self.msg, 'name': f"111的{ss['catch']},"+ss['type']+str(ss['exp_val'])})

            else:
                if ss['method']=='log':
                    self.run_log.append(self._local_catch(ss))
                else:
                    self.run_log.append(
                    {'status': '未运行', 'msg': '前置步骤出错', 'name': f"期望提取值的{ss['catch']},"+ss['type']+str(ss['exp_val'])})
        else:
            self.catch_log.append(ss)

    def _params_trans(self):
        # 把参数填充
        da = json.dumps(self.data, ensure_ascii=False)
        v1 = re.findall(r"\$\{(.+?)\}", da)
        for i in v1:
            if i in self.my_dict:
                if isinstance(self.my_dict[i], str):
                    self.params[i] = self.my_dict[i]
                    da = da.replace('${'+i+'}', self.my_dict[i])
                elif isinstance(self.my_dict[i], dict) or isinstance(self.my_dict[i], list):
                    d2 = json.dumps(self.my_dict[i], ensure_ascii=False)
                    self.params[i] = d2
                    da = da.replace('"${'+i+'}"', d2)
                    da = da.replace('${'+i+'}', d2)
                else:
                    d2 = str(self.my_dict[i])
                    self.params[i] = d2
                    da = da.replace('${'+i+'}', d2)
            elif '.' in i:
                ii = i.split('.')
                v = ''
                if ii[0] in self.my_dict:
                    v = self.my_dict[ii[0]]
                    ii.pop(0)
                else:
                    continue
                if isinstance(v, dict) or isinstance(v, list):
                    for i2 in ii:
                        if isinstance(v, list):
                            try:
                                v = v[int(i2)]
                            except:

                                self.msg = str(v)+'中提取'+str(i2)+',失败'
                                self.self_status = False
                                self.run_log.append(
                                    {'status': '失败', 'msg': self.msg, 'name': f"运行前01：参数转化"})
                                return
                        elif isinstance(v, dict):

                            if i2 in v:
                                v = v[i2]
                            else:

                                self.msg = str(v)+'中提取'+str(i2)+',失败'
                                self.self_status = False
                                self.run_log.append(
                                    {'status': '失败', 'msg': self.msg, 'name': f"运行前02：参数转化"})
                                return
                        else:

                            self.msg = str(v)+'中提取'+str(i2)+',失败'
                            self.self_status = False
                            self.run_log.append(
                                {'status': '失败', 'msg': self.msg, 'name': f"运行前03：参数转化"})
                            return

                if isinstance(v, str):
                    self.params[i] = v
                    da = da.replace('${'+i+'}', v)
                elif isinstance(v, dict) or isinstance(v, list):
                    d2 = json.dumps(v, ensure_ascii=False)
                    self.params[i] = d2
                    da = da.replace('${'+i+'}', d2)
                else:
                    d2 = str(v)
                    self.params[i] = d2
                    da = da.replace('${'+i+'}', d2)
        try:
            self.data_pre = json.loads(da)
        except Exception as e:
            self.msg = str(e)+'-------'+da
            self.self_status = False
            self.run_log.append(
                {'status': '失败', 'msg': self.msg, 'name': f"运行前04：参数转化"})

    def run(self, func=None):
        if 'imtby'  in sys.argv:
            self.res={}
            self.req={}
            self.params={}
            self.run_log=[]
            self.is_run=False


        # 检查传入值是否带方法
        if func is not None:
            self.func_instance = func
        # 检查方法是否可运行
        if self.func_instance is None:
            logger.error('请使用addFunc方法传入实例')
            self.msg = '没有运行实例'
            self.self_status = False
            self.run_log.append(
                {'status': '失败', 'msg': self.msg, 'name': f"运行前：检查实例"})
        else:
            # 判断方法方法是否值得执行
            for i in self.catch_log:
                if not i['status']:
                    self.msg = i['msg']
                    self.self_status = False
                    self.run_log.append(
                        {'status': '失败', 'msg': self.msg, 'name': f"运行前：检查判断条件"})
                    return self

            # 处理参数化
            self._params_trans()

            if self.self_status:
                if self.reqf is not None:
                    try:
                        self.data_pre, self.local, self.globals = self.reqf(
                            self.data_pre, self.local, self.globals)
                    except Exception as e:
                        self.status = '失败'
                        self.msg = '运行方法错误：输入值为req,lcoal,gloabls,输出同样也是。例子：def(req,mylocal,myglobals) -> req,mylocal,myglobals;'+str(
                            e)
                        self.run_log.append(
                            {'status': self.status, 'msg': self.msg, 'name': "运行前："+self.label})
                        self.is_run = False
                        return self

                self.start_time = time.time()
                self.func_instance.run(**self.data_pre)
                self.end_time = time.time()
                self.req = self.func_instance.req
                if self.func_instance.status:
                    self.status = '成功'
                    self.res = self.func_instance.res
                    if self.resf is not None:
                        try:
                            self.res, self.local, self.globals = self.reqf(
                                self.res, self.local, self.globals)
                        except Exception as e:
                            self.status = '失败'
                            self.msg = '运行方法错误：输入值为res,lcoal,gloabls,输出同样也是。例子：def(res,mylocal,myglobals) -> res,mylocal,myglobals;'+str(
                                e)
                            self.run_log.append(
                                {'status': self.status, 'msg': self.msg, 'name': "运行后："+self.label})
                            self.is_run = False
                            return self

                else:
                    self.status = '失败'
                    self.msg = self.func_instance.e
                self.run_log.append(
                    {'status': self.status, 'msg': self.msg, 'name': "运行："+self.label})
                if 'imtby' not in sys.argv:
                    self.is_run = True
                for i in self.catch_log:
                    if self.status == '成功' and self.self_status:
                        # self.run_log.append({'status':'成功','msg':i['msg'],'name':"期望："+i['type']+str(i['exp_val'])})
                        # self.run_log.append({'status':'失败','msg':i['msg'],'name':"期望："+i['type']+str(i['exp_val'])})

                        self.run_log.append(self._local_catch(i))
                    else:
                        if i['method']=='log':
                            self.run_log.append(self._local_catch(i))
                        else:
                            self.run_log.append(
                            {'status': '未运行', 'msg': '前置步骤出错', 'name': f"期望提取值的{i['catch']},"+i['type']+str(i['exp_val'])})
            return self

    def _local_catch(self, val):

        try:
            if val['status']:

                if val['method'] == 'json':
                    if isinstance(self.res, dict):
                        res = self.res

                    elif isinstance(self.res, str):
                        try:
                            res = json.loads(self.res)
                        except:
                            self.self_status = False
                            self.status = '失败'
                            self.msg = '期望结果为json格式，但实际为不可转化的字符串'
                            return {'status': '失败', 'msg': self.msg, 'name': f"02期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                    elif isinstance(self.res, list):
                        res = self.res
                    else:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '期望结果为json格式，但实际为其他格式'
                        return {'status': '失败', 'msg': self.msg, 'name': f"03期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                    if val['catch'] is None or not val['catch'] or len(val['catch'].strip()) == 0:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '提取方式为json，无法提取对应的值，方法为：' + \
                            str(val['catch'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"04期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                    else:
                        cas = str(val['catch']).split('.')
                        for i in cas:
                            if isinstance(res, dict):
                                if i in res:
                                    # print(i)
                                    # print(res)
                                    res = res[i]
                                else:
                                    self.self_status = False
                                    self.status = '失败'
                                    self.msg = '提取方式为json，无法提取对应的值，方法为：' + \
                                        str(val['catch'])
                                    return {'status': '失败', 'msg': self.msg, 'name': f"05期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                            elif isinstance(res, list):
                                try:
                                    i = int(i)
                                except:
                                    self.self_status = False
                                    self.status = '失败'
                                    self.msg = '提取方式为json，期望为数字，实际为{}，方法为：'.format(
                                        str(i))+str(val['catch'])
                                    return {'status': '失败', 'msg': self.msg, 'name': f"06期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                                if len(res) > i:
                                    res = res[i]
                                else:
                                    self.self_status = False
                                    self.status = '失败'
                                    self.msg = '提取方式为json，结果值{}无法满足期望值{}，方法为：'.format(
                                        str(len(res)), str(i)).format(str(i))+str(val['catch'])
                                    return {'status': '失败', 'msg': self.msg, 'name': f"07期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                            else:
                                self.self_status = False
                                self.status = '失败'
                                self.msg = '提取结果失败，结果格式为{}，方法为：'.format(
                                    str(type(res)))+str(val['catch'])
                                return {'status': '失败', 'msg': self.msg, 'name': f"08期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['method'] == 'regex':
                    res = str(self.res)
                    ress = re.findall(val['catch'], res)
                    if len(ress) == 1:
                        res = ress[0]
                    else:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '正则提取结果失败，结果数量为：{}，方法为：'.format(
                            str(len(ress)))+str(val['catch'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"09期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['method'] == 'size':
                    res = len(self.res)
                elif val['method'] == 'log':
                    if self.is_print:
                        
                        print('-'*15, '运行结果', '-'*15)
                        print(self.val_dict())
                        print()
                        print('-'*15, '运行步骤结果', '-'*15)
                        print(self.run_log)
                        print()
                        print('-'*15, '请求数据', '-'*15)
                        print(self.req)
                        print()
                        print('-'*15, '响应数据', '-'*15)
                        print(self.res)
                        print()
                        print('-'*15, '环境值（私有）', '-'*15)
                        print(self.local)
                        print()
                        print('-'*15, '环境值（公共）', '-'*15)
                        print(self.globals)
                        print()
                        print('-'*15, '参数使用', '-'*15)
                        print(self.params)
                        print('-'*15, '结束', '-'*15)

                    return {'status': '成功', 'msg': '显示信息', 'name': self.label}
                else:
                    self.self_status = False
                    self.status = '失败'
                    self.msg = '提取方法未知，方法为：'+str(val['catch'])
                    return {'status': '失败', 'msg': self.msg, 'name': f"10期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                if val['type'] == '等于':
                    if res == val['exp_val']:
                        return {'status': '成功', 'msg': '', 'name': f"11期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                    else:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '实际结果为：'+str(res)
                        return {'status': '失败', 'msg': self.msg, 'name': f"12期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '不等于':
                    if res == val['exp_val']:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '结果相等'
                        return {'status': '失败', 'msg': self.msg, 'name': f"13期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        return {'status': '成功', 'msg': '', 'name': f"14期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '不为空':
                    if res is None or res == '':
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '结果为空'
                        return {'status': '失败', 'msg': self.msg, 'name': f"15期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        return {'status': '成功', 'msg': '', 'name': f"16期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '为空':
                    if res is not None and res != '':
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '结果不为空'
                        return {'status': '失败', 'msg': self.msg, 'name': f"17期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        return {'status': '成功', 'msg': '', 'name': f"18期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '>':
                    try:
                        va = int(val['exp_val'])
                    except:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '期望值不为数字，无法比较大小,'+str(val['exp_val'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"19期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                    try:
                        va2 = int(res)
                    except:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '结果值不为数字，无法比较大小,'+str(res)
                        return {'status': '失败', 'msg': self.msg, 'name': f"20期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    if va2 > va:
                        return {'status': '成功', 'msg': '', 'name': f"21期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = f'结果值{str(va2)}不大于期望值{str(va)}'
                        return {'status': '失败', 'msg': self.msg, 'name': f"22期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                elif val['type'] == '>=':
                    try:
                        va = int(val['exp_val'])
                    except:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '期望值不为数字，无法比较大小,'+str(val['exp_val'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"23期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                    try:
                        va2 = int(res)
                    except:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '结果值不为数字，无法比较大小,'+str(res)
                        return {'status': '失败', 'msg': self.msg, 'name': f"24期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    if va2 >= va:
                        return {'status': '成功', 'msg': '', 'name': f"25期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = f'结果值{str(va2)}小于期望值{str(va)}'
                        return {'status': '失败', 'msg': self.msg, 'name': f"26期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '<':
                    try:
                        va = int(val['exp_val'])
                    except:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '期望值不为数字，无法比较大小,'+str(val['exp_val'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"27期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                    try:
                        va2 = int(res)
                    except:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '结果值不为数字，无法比较大小,'+str(res)
                        return {'status': '失败', 'msg': self.msg, 'name': f"28期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    if va2 < va:
                        return {'status': '成功', 'msg': '', 'name': f"29期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = f'结果值{str(va2)}不小于期望值{str(va)}'
                        return {'status': '失败', 'msg': self.msg, 'name': f"30期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '<=':
                    try:
                        va = int(val['exp_val'])
                    except:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '期望值不为数字，无法比较大小,'+str(val['exp_val'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"31期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                    try:
                        va2 = int(res)
                    except:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = '结果值不为数字，无法比较大小,'+str(res)
                        return {'status': '失败', 'msg': self.msg, 'name': f"32期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    if va2 <= va:
                        return {'status': '成功', 'msg': '', 'name': f"33期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = f'结果值{str(va2)}大于期望值{str(va)}'
                        return {'status': '失败', 'msg': self.msg, 'name': f"34期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '匹配':
                    if re.match(str(val['exp_val']), str(res)) is None:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = f'结果值{str(res)}无法匹配正则:'+str(val['exp_val'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"35期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        return {'status': '成功', 'msg': '', 'name': f"36期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '不匹配':
                    if re.match(str(val['exp_val']), str(res)) is not None:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = f'结果值{str(res)}匹配正则:'+str(val['exp_val'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"37期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        return {'status': '成功', 'msg': '', 'name': f"38期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '包含':
                    if val['exp_val'] not in res:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = f'结果值{str(res)}不包含期望值:'+str(val['exp_val'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"39期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        return {'status': '成功', 'msg': '', 'name': f"40期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '不包含':
                    if val['exp_val'] in res:
                        self.self_status = False
                        self.status = '失败'
                        self.msg = f'结果值{str(res)}包含期望值:'+str(val['exp_val'])
                        return {'status': '失败', 'msg': self.msg, 'name': f"41期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

                    else:
                        return {'status': '成功', 'msg': '', 'name': f"42期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                elif val['type'] == '保存':
                    if val['is_global']:
                        self.globals[val['exp_val']] = res
                        return {'status': '成功', 'msg': '全局:'+str(res), 'name': f"43期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
                    else:
                        self.local[val['exp_val']] = res
                        return {'status': '成功', 'msg': '本地:'+str(res), 'name': f"44期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

            else:
                self.self_status = False
                self.status = '失败'
                self.msg = val['msg']
                return {'status': '失败', 'msg': str(val['msg']), 'name': f"45期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}
        except Exception as e:
            return {'status': '失败', 'msg': str(e), 'name': f"46期望提取值的{val['catch']},"+val['type']+str(val['exp_val'])}

    def addLocal(self, local: dict, glo: dict):
        self.globals = glo
        self.local = local
        self.my_dict.update(glo.copy())
        self.my_dict.update(local.copy())
        if self.func in self.local:
            if isinstance(self.local[self.func], baseClass):
                self.func_instance = self.local[self.func]

        return self

    def save(self,  catch: str, name: str, method: str = 'json', is_global=False):
        msg = ''
        status = True
        cmd = {}
        if method == 'json':
            pass
        elif method == 'regex':
            pass
        elif method == 'length':
            pass
        else:
            status = False
            msg = 'expect方式使用错误，method参数填写错误'

        cmd['method'] = method
        cmd['catch'] = catch
        cmd['status'] = status
        cmd['msg'] = msg
        cmd['exp_val'] = name
        cmd['type'] = '保存'
        cmd['is_global'] = is_global

        if self.is_run:
            if self.status == '成功' and self.self_status:
                if cmd['status']:

                    self.run_log.append(self._local_catch(cmd))
                else:
                    self.self_status = False
                    self.status = '失败'
                    self.msg = msg
                    return {'status': '失败', 'msg': self.msg, 'name': f"期望提取值的{cmd['catch']},"+cmd['type']+str(cmd['exp_val'])}

            else:
                self.run_log.append(
                    {'status': '未运行', 'msg': '前置步骤出错', 'name': f"期望提取值的{cmd['catch']},"+cmd['type']+str(cmd['exp_val'])})

        else:
            self.catch_log.append(cmd)
        return self

    def back(self, func):
        def cc(*v, **k):
            if func is None:
                return self
            elif isinstance(func, str):
                if self.is_run:
                    self.run_log.append(
                        {'status': '未运行', 'msg': '无此方法:'+func, 'name': "方法调用失败："+func})
                else:
                    self.catch_log.append({'method': 'err', 'catch': '', 'run': False, 'status': False,
                                           'msg': '无此方法:'+func, 'exp_val': None, 'type': '代码出错', 'paras_list': list(v), 'para_dict': k})

                return self
            else:
                try:
                    return func(*v, **k)
                except:
                    return self

        return cc

    def __getattr__(self, attr):

        return self.back(attr)

    def expect(self, catch: str, method: str = 'json'):
        '''
        method json regex size
        '''
        # res=None
        msg = ''
        status = True
        cmd = {}
        if method == 'json':
            pass
        elif method == 'regex':
            pass
        elif method == 'size':
            pass
        else:
            status = False
            msg = 'expect方式使用错误，method参数填写错误'

        cmd['method'] = method
        cmd['catch'] = catch
        cmd['status'] = status
        cmd['msg'] = msg

        return checkRes(cmd, self)


class checkRes:
    def __init__(self, data, func=None):
        self.data = data
        self.func = func

    def __getattr__(self, attr):

        if attr in self.func.__dict__:
            return self.func.__dict__[attr]

        else:

            try:
                if self.func.__getattribute__(attr) is not None:
                    if self.data['run']:
                        pass
                    else:
                        self.data['exp_val'] = '方法没有输入期望的值'
                        self.data['type'] = '代码出错'
                        self.data['msg'] = '方法没有输入期望的值'
                        self.data['status'] = False
                        self.func._add_catch_log(self.data)

                        return self.func.back(self.func.__getattribute__(attr))
            except:

                return self.func.back(str(attr))

    def toBe(self, val):
        self.data['exp_val'] = val
        self.data['type'] = '等于'
        self.func._add_catch_log(self.data)
        return self.func

    def notToBe(self, val):
        self.data['exp_val'] = val
        self.data['type'] = '不等于'
        self.func._add_catch_log(self.data)
        return self.func

    def notToBeNone(self):
        self.data['exp_val'] = ''
        self.data['type'] = '不为空'
        self.func._add_catch_log(self.data)
        return self.func

    def toBeNone(self):
        self.data['exp_val'] = ''
        self.data['type'] = '为空'
        self.func._add_catch_log(self.data)
        return self.func

    def toBeTruthy(self):
        self.data['exp_val'] = True
        self.data['type'] = '等于'
        self.func._add_catch_log(self.data)
        return self.func

    def toBeFalsy(self):
        self.data['exp_val'] = False
        self.data['type'] = '等于'
        self.func._add_catch_log(self.data)
        return self.func

    def toBeGreaterThanOrEqual(self, num):
        self.data['exp_val'] = num
        self.data['type'] = '>='
        self.func._add_catch_log(self.data)
        return self.func

    def toBeGreaterThan(self, num):
        self.data['exp_val'] = num
        self.data['type'] = '>'
        self.func._add_catch_log(self.data)
        return self.func

    def toBeLessThan(self, num):
        self.data['exp_val'] = num
        self.data['type'] = '<'
        self.func._add_catch_log(self.data)
        return self.func

    def toBeLessThanOrEqual(self, num):
        self.data['exp_val'] = num
        self.data['type'] = '<='
        self.func._add_catch_log(self.data)
        return self.func

    def toMatch(self, val):
        self.data['exp_val'] = val
        self.data['type'] = '匹配'
        self.func._add_catch_log(self.data)
        return self.func

    def notToMatch(self, val):
        self.data['exp_val'] = val
        self.data['type'] = '不匹配'
        self.func._add_catch_log(self.data)
        return self.func

    def toContain(self, val):
        self.data['exp_val'] = val
        self.data['type'] = '包含'
        self.func._add_catch_log(self.data)
        return self.func

    def notToContain(self, val):
        self.data['exp_val'] = val
        self.data['type'] = '不包含'
        self.func._add_catch_log(self.data)
        return self.func


def fetch(url, data, replace=None):
    dd = {}
    dd['url'] = url
    dd['method'] = data['method']
    dd['headers'] = data['headers']
    if replace is None:
        dd['data'] = data['body']
    else:
        dd['data'] = replace
    return dd

def raw(sss):
    aa=sss.strip().strip('\n').split('\n')
    d={'data':'','headers':{}}
    is_start=False
    is_body=False
    for i in aa:
        if not is_start:
            if len(i.strip())>0:
                is_start=True
                v=i.strip().split(' ')
                d['method']=v[0]
                d['url']=v[1]
        else:
            if  is_body:
                d['data']+=i
            elif  len(i.strip())>0:
                try:
                    vv=i.split(': ')
                    d['headers'][str(vv[0])]=str(vv[1])
                except :
                    pass
            else:
                is_body=True
    return d




# a = item('name1', 'http', fetch("https://paytest.ciicsh.com/auth/authenticate/login", {
#     "headers": {
#         "accept": "application/json, text/plain, */*",
#         "accept-language": "zh-CN,zh;q=0.9",
#         "content-type": "application/json;charset=UTF-8",
#         "sec-fetch-dest": "empty",
#         "sec-fetch-mode": "cors",
#         "sec-fetch-site": "same-origin"
#     },
#     "referrer": "https://paytest.ciicsh.com/login?redirect=%2Fapproval%2FtoDoList",
#     "referrerPolicy": "no-referrer-when-downgrade",
#     "body": "{\"userId\":\"${uid}\",\"password\":\"${pawd}\"}",
#     "method": "POST",
#     "mode": "cors",
#     "credentials": "omit"
# }))
# # .expect('asda.sd.a.sd','json').toBe1(123).save('asda.sd.a.sd','json','1231')
# a.addLocal({'uid': 13800126000, 'pawd': 'AAAaaa111'}, {})
# a.addFunc(DoRequest()).expect('status_code', 'json').toBe(200).expect('data.code', 'json').toBe(0).run().save('data.token','json','token')
# print(a)
# # print(a.req)
# # print(a.res)
# # print(3,a.labal)
# # print(3,a.catch_log)
# print(a.local)
# # print(a.params)
# # print(a.data)
# # print(a.data_pre)
# print(a.run_log)
