# -*- coding:utf-8 -*-
# Author:lixuecheng

import pymssql
from requestQ.package.logger import log, logger
from requestQ.package.baseClass import baseClass



class DoMssql(baseClass):
    @log
    def __init__(self, ip, user, password, dbname, port=1433,is_autocommit=True):
        try:
            self.ip = ip
            self.port = port
            self.user = user
            self.password = password
            self.dbname = dbname
            self.db = pymssql.connect(host=self.ip, port=int(self.port), user=self.user, password=self.password,
                                      database=self.dbname,
                                      charset='utf8',
                                      autocommit=False,as_dict=True)
            self.string = self.ip + ':' + str(
                self.port) + ',user=' + self.user + ',password=' + self.password + ',database=' + self.dbname
            self.cursor = self.db.cursor()
            self.status = True
            self.is_auto=is_autocommit
            self.res=[]
            logger.info('mssql连接成功，-----' + self.string)
        except Exception as e:
            self.db = None
            self.cursor = False
            self.e = e
            self.string = str(e)
            self.status = False
            raise Exception('数据库连接失败：' + str(e))

    def __str__(self):
        try:
            return 'mysql_' + self.string
        except Exception as e:

            # logger.warn('mysql字符串转化失败，' + str(e))
            return 'mysql,无字符串初始化，获取是日志获取中发生,' + str(e)
            # raise Exception('mysql字符串转化失败，' + str(e))

    @log
    def run(self, sql:str) -> int:

        if self.cursor and self.status:
            try:
                self.sql=sql
                self.cursor.execute(sql)
                
                self.res = self.cursor.fetchall()
                if self.is_auto:
                    self.commit()
              
                return self.cursor.rowcount
            except Exception as e:
                self.e = e
                raise Exception(sql+',执行sql失败，' + e.__str__())

        else:
            raise Exception('数据库链接失败')

    def close(self):
        try:
            self.cursor.close()
            self.db.close()
        except:
            pass
        self.status = False
        # logger.info('数据库断开连接')

    def commit(self):
        logger.info('执行数据库提交')
        self.db.commit()


    def rollback(self):
        logger.info('执行数据库回滚,' + str(self.e))
        self.db.rollback()

