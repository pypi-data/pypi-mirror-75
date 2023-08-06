# -*- coding:utf-8 -*-
# Author:lixuecheng


from requests import session, Request
from requestQ.package.baseClass import baseClass
from requestQ.package.logger import log, logger
from requestQ.config.sys_config import text_type, json_type
import os
import json
from urllib3 import encode_multipart_formdata


class DoRequest(baseClass):

    def __init__(self):
        self.s = session()
        # 配置默认请求头信息
        self.s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'

        self.e = '未执行'  # 存储报错信息
        self.req = {}  # 存储请求信息
        self.res = {}  # 存储结果信息
        self.status = False  # 标注请求状态
        self.is_commit = False

    def add_session_headers(self,dict_headers):
        if isinstance(dict_headers,dict):
            self.s.headers.update(dict_headers)
        else:
            self.e='添加请求头信息不是字典类型'

    @log
    def run(self, method: str, url: str, data=None, is_auto=True, **kwargs):
        '''
        运行请求
        :param method    
        请求方法 使用 post get 等
        :param url  
        请求链接 请加上http 或者https
        :param  data 
        支持str，dict，"xxx=yyy&sss=www"的方式
        :param  is_auto 
        默认True，当False时，需要使用commit发送请求
        :param kwargs 
        支持部分配置
            ：val  files 格式str,上传文件的路径 
            ：val  file_name 格式str,用于设置上传文件名称，不填默认文件名称
            ：val  headers 格式dict,{xxx:yyy,sss:www} 设置请求头
            : val  proxies 设置请求代理 格式 ip:port

        '''
        try:
            self._check_proxies(kwargs)  # 检查是否有代理信息
            self.req['method'] = method.upper()  # 记录请求方法
            self.req['url'] = self._check_url(url)  # 记录url,检查请求方式
            self.req['data'] = self._check_data(data)  # 记录请求体，检查并转化请求体的值为字符串
            self.req['files'] = self._get_file(kwargs)  # 检查是否有上传文件
            self.req['headers'] = self.s.headers  # 初始化请求头
            self._check_headers(kwargs)  # 检查是否有配置请求头
            req = Request(**self.req)  # 组装请求信息
           
            self.req_pre = self.s.prepare_request(req)  # 检查请求值是否满足要求
          
            self.status = True  # 确认状态，可执行
            self.e = ''  # 记录异常
            self.is_commit = False  # 修改提交状态
            logger.info(str(self.req))

        except Exception as e:
            self.e = str(e)
            self.status = False  # 确认状态，不可执行
        if is_auto:
            return self.commit()  # 提交请求
        else:
            return self

    def commit(self):
        if self.status:
            try:
                if self.is_commit:
                    return '请勿重复提交'

                self.res_value = self.s.send(
                    self.req_pre, proxies=self.proxies)  # 发送并接受请求
                self.is_commit = True
                # 记录响应结果
                self.res['status_code'] = int(self.res_value.status_code)
                self.res['content'] = self.res_value.content
                self.res['elapsed'] = str(self.res_value.elapsed)
                self.res['encoding'] = str(self.res_value.encoding)
                self.res['history'] = self.res_value.history
                self.res['reason'] = str(self.res_value.reason)
                self.res['headers'] = self.res_value.headers
                self.res['url'] = str(self.res_value.url)
                t, f, da = self._value()  # 解析响应结果
                self.res['data'] = da
                self.res['header_type'] = {'type': t, 'info': f}  # 记录响应值得格式
                self.status = True
                self.e = ''
                del self.res['content']
                logger.info(str(self.res))
                # print(self.res)
                return da
            except Exception as e:

                self.e = str(e)
                self.status = False
                return self.e

        else:
            return '请求有错误，请检查:'+self.e


    def get_req_info(self):
        if self.status:
            return self.req
        else:
            return self.e

    def get_res_info(self):
        if self.status:
            return self.res
        else:
            return self.e

    def _value(self, encoding='utf8'):
        if self.status:
            if 'Content-Type' in self.res['headers']:
                a = self.res['headers']['Content-Type'].split(';')
                
                if a[0].strip() in json_type:

                    if len(a) == 2 and a[1].strip().startswith('charset='):

                        type = a[1].strip().replace('charset=', '')
                        text = self.res['content'].decode(type)

                        return 'json', self.res['headers']['Content-Type'], json.loads(text)
                    else:

                        return 'json', self.res['headers']['Content-Type'], json.loads(self.res['content'].decode(encoding))
                elif a[0].strip() in text_type:
                    if len(a) == 2 and a[1].strip().startswith('charset='):


                        type = a[1].strip().replace('charset=', '')
                        text = self.res['content'].decode(type)

                        return 'text', self.res['headers']['Content-Type'], text
                    else:

                        return 'text', self.res['headers']['Content-Type'], self.res['content'].decode(encoding)
                else:

                    return 'byte', self.res['headers']['Content-Type'], self.res['content']

            else:

                return 'byte', None, self.res['content']
        else:
            raise Exception('前置请求有错误，请检查')
            # if self.need_exception:
            #         raise Exception("请求执行错误，当前方法无法执行")
            # else:
            #     self.status=False
            #     return False,"请求执行错误，当前方法无法执行"

    def _check_url(self, url: str) -> str:
        if str(url).lower().startswith('http'):
            return str(url)
        else:
            raise Exception(str(url)+',连接没有请求方式，请添加http://或者https://')

    def _check_data(self, data) -> str:
        if data is None:
            return None
        elif isinstance(data, bytes):
            return data.decode('utf8').encode()
        else:
            if isinstance(data, str):
                return data.encode()
            elif isinstance(data, dict):
                return json.dumps(data, ensure_ascii=False).encode()
            else:
                raise Exception('请求内容是格式不在支持范围内，请使用字符串'+str(data))

    def _get_file(self, kwargs):
        file_dict = {}
        if kwargs.get('files') is not None and len(kwargs.get('files')) > 0:
            f = kwargs.get('files')

            if isinstance(f, str):
                if os.path.exists(f):
                    if kwargs.get('file_name') is not None and len(kwargs.get('file_name')) > 0:
                        file_dict[str(kwargs.get('file_name'))] = f
                    else:
                        file_dict[os.path.basename(f)] = f

                else:
                    raise FileNotFoundError(f)
            elif isinstance(f, dict) or isinstance(f, list):
                # TODO
                raise Exception('暂时不支持多个文件上传')
            else:
                raise Exception('暂时只支持字符串类型')
        return file_dict

    def _check_proxies(self, kwargs):
        if kwargs.get('proxies') is not None and len(kwargs.get('proxies')) > 0:
            d = kwargs.get('proxies')
            if isinstance(d, dict):

                self.proxies = d
            elif isinstance(d, str):
                if d.startswith('http'):
                    self.proxies = {"http": d, "https": d}
                else:
                    self.proxies = {
                        "http": 'http://'+d, "https": 'http://'+d}
            else:
                raise Exception(
                    '代理格式不正确，请检查，使用：{"http": http://xxxx, "https": http://xxxx} 或者 http://xxxxx')
        else:
            self.proxies = None

    def _check_headers(self, kwargs):

        is_multipart = False
        if kwargs.get('headers') is not None and len(kwargs.get('headers')) > 0:
            d = kwargs.get('headers')
            if isinstance(d, dict):
                self.req['headers'].update(d)
            else:
                raise Exception(
                    '请求头信息不正确，请检查，使用：{"xxx": xxx, "xxxx": xxxx}')
            if 'Content-Type' in d:
                if d['Content-Type'].lower().startswith('multipart'):
                    is_multipart = True

        if 'Content-Type' not in self.req['headers']:

            if self.req['method'] == 'POST' or self.req['method'] == 'PUT':
                if len(self.req['files']) > 0:
                    is_multipart = True

                elif self.req['data'].startswith(b'{') or self.req['data'].startswith(b'['):
                    self.req['headers']['Content-Type'] = 'application/json;charset=UTF-8'
                else:
                    self.req['headers']['Content-Type'] = 'application/x-www-form-urlencoded'

        if is_multipart:
            if len(self.req['files']) > 0:
                is_multipart = True
                files = {}
                for i in self.req['files']:
                    files[i] = (os.path.basename(self.req['files'][i]), open(
                        self.req['files'][i], 'rb').read())
                self.req['data'].update(files)
            encode_data = encode_multipart_formdata(
                json.loads(self.req['data']))
            self.req['headers']['Content-Type'] = encode_data[1]
            self.req['data'] = encode_data[0]


