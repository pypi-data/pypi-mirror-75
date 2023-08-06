# -*- coding:utf-8 -*-
# Author:lixuecheng
# from request.package.item import item
from requestQ.package.dorequest import DoRequest
from requestQ.package.logger import color_print
import sys

my_globals = {}


class Case:
    def __init__(self, name, *items):
        self.name = name
        self.items = items
        self.local = {}
        self.source = {'http': DoRequest()}
        self.res = []
        self.status = '未运行'
        self.step = {}
        self.msg = ''

    def run(self, allow_print_detail=False, allow_print_res=True):
        '''
        allow_print_detail 默认false ，用于打印item信息
        allow_print_res 默认 true，用于打印简单结果
        '''
        if 'imtby' not in sys.argv:
            sys.argv.append('imtby')
        if allow_print_res:
            color_print({'type': 'warn', 'val': '> '+str(self.name)})

        for it in self.items:
            if it.is_run:
                self.res.append(it.val_dict())
                self.step[it.id] = it.run_log
                my_globals.update(it.globals)
                self.local.update(it.local)
                self.status = '成功'
                if it.status != '成功':
                    self.status = '失败'
                if allow_print_res:
                    tt = ''
                    if it.status == '成功':
                        tt = {'type': 'success', 'val': '成功'}
                    elif it.status == '失败':
                        tt = {'type': 'err', 'val': '失败'}
                    elif it.status == '未运行':
                        tt = {'type': 'normal', 'val': '未运行'}
                    else:
                        tt = {'type': '', 'val': ''}
                    vv = '   '+it.label
                    vv += '~'+it.msg
                    if self.status == '错误':
                        tt = {'type': 'err', 'val': '失败'}
                        vv += '~'+self.msg

                    color_print({'type': '', 'val': 'r\t'}, tt, {'val': vv})

            elif it.func in self.source:
                try:
                    if self.status != '失败' or self.status != '错误':
                        it.is_print = allow_print_detail
                        if it.is_print:
                            for cc in it.catch_log:
                                if cc['method']=='log':
                                    break
                            else:
                                it.catch_log.append({'method': 'log', 'status': True})

                        t = it.addLocal(self.local, my_globals).run(
                            self.source[it.func])

                        self.res.append(t.val_dict())
                        self.step[t.id] = t.run_log
                        my_globals.update(t.globals)
                        self.local.update(t.local)
                        self.status = '成功'
                        if t.status != '成功':
                            self.status = '失败'
                    else:
                        self.res.append(t.val_dict())

                except Exception as e:
                    self.status = "错误"
                    self.msg = '存在非用例的错误：'+str(e)
                if allow_print_res:
                    tt = ''
                    if it.status == '成功':
                        tt = {'type': 'success', 'val': '成功'}
                    elif it.status == '失败':
                        tt = {'type': 'err', 'val': '失败'}
                    elif it.status == '未运行':
                        tt = {'type': 'normal', 'val': '未运行'}
                    else:
                        tt = {'type': '', 'val': ''}
                    vv = '   '+it.label
                    vv += '~'+it.msg
                    if self.status == '错误':
                        tt = {'type': 'err', 'val': '失败'}
                        vv += '~'+self.msg

                    color_print({'type': '', 'val': 'n\t'}, tt, {'val': vv})

            else:
                if allow_print_res:
                    color_print({'type': '', 'val': 'n\t'}, {
                                'type': 'err', 'val': '没有找到实际运行对象'})

        if 'imtby' in sys.argv:
            sys.argv.remove('imtby')
        return self

    def add_source(self, source, name):
        self.source[name] = source


class Cases:
    def __init__(self, *ca):
        for i in ca:
            i.run(False)
