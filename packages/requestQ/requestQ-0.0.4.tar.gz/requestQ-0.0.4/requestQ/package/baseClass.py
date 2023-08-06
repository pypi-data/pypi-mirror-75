# -*- coding:utf-8 -*-
# Author:lixuecheng

class baseClass(object):
    def __init__(self,*args, **kwargs):
        self.string=''
        self.req={}
        self.status=True
        self.res={}
        self.e=''

    def run(self,*args, **kwargs):
        pass

    def commit(self,*args, **kwargs):
        pass

    def rollback(self,*args, **kwargs):
        pass

    def check(self, *args, **kwargs):
        pass

    def close(self):
        pass

    def __str__(self):
        try:
            return self.string
        except:
            return ''
