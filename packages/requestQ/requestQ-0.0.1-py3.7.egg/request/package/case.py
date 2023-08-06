# -*- coding:utf-8 -*-
# Author:lixuecheng
# from request.package.item import item
from request.package.dorequest import DoRequest

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

    def run(self):
        for it in self.items:
            if it.func in self.source:
                try:
                    if self.status != '失败' or self.status != '错误':
                        t = it.addLocal(self.local, my_globals).run(
                            self.source[it.func])

                        self.res.append(t.val_dict())
                        self.step[t.id] = t.run_log
                        my_globals.update(t.globals)
                        self.local.update(t.local)
                        self.status='成功'
                        if t.status != '成功':
                            self.status = '失败'
                    else:
                        self.res.append(t.val_dict())

                except Exception as e:
                    self.status = "错误"
                    self.msg = '存在非用例的错误：'+str(e)

            else:
                print('没有找到实际运行对象')
                
        print(self.status,self.msg)
        return self

    def add_source(self, source, name):
        self.source[name] = source
