# -*- coding:utf-8 -*-
# Author:lixuecheng
# from request.package.item import item
from requestQ.package.dorequest import DoRequest
from requestQ.package.logger import color_print

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

    def run(self,allow_print_detail=False,allow_print_res=True):
        '''
        allow_print_detail 默认false ，用于打印item信息
        allow_print_res 默认 true，用于打印简单结果
        '''
        if allow_print_res:
            color_print({'type':'warn','val':'> '+str(self.name)})

        for it in self.items:
            if it.func in self.source:
                try:
                    if self.status != '失败' or self.status != '错误':
                        it.is_print=allow_print_detail
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
                if allow_print_res:
                    tt=''
                    if it.status=='成功':
                        tt={'type':'success','val':'成功'}
                    elif it.status=='失败':
                        tt={'type':'err','val':'失败'}
                    elif it.status=='未运行':
                        tt={'type':'normal','val':'未运行'}
                    else:
                        tt={'type':'','val':''}
                    vv='   '+it.label
                    vv+='~'+it.msg
                    if self.status=='错误':
                        tt={'type':'err','val':'失败'}
                        vv+='~'+self.msg

                    
                    color_print({'type':'','val':'\t'},tt,{'val':vv})


            else:
                if allow_print_res:
                    color_print({'type':'','val':'\t'},{'type':'err','val':'没有找到实际运行对象'})
      
                
        return self

    def add_source(self, source, name):
        self.source[name] = source

class Cases:
    def __init__(self,*ca):
        for i in ca:
            i.run(False)

