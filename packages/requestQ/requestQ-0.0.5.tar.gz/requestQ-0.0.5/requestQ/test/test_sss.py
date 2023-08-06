sss='''
POST https://paytest.ciicsh.com/auth/authenticate/login HTTP/1.1
Host: paytest.ciicsh.com
Connection: keep-alive
Content-Length: 47
Accept: application/json, text/plain, */*
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
Content-Type: application/json;charset=UTF-8
Origin: https://paytest.ciicsh.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://paytest.ciicsh.com/login?redirect=%2FtimeManagement%2FattendanceRule
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=8DEFAC5E90EEBC91C33AA744798114B2

{"userId":"13800920000","password":"AAAaaa111"}
'''
aa=sss.strip().strip('\n').split('\n')
n=1
d={'body':'','headers':{}}
is_start=False
is_body=False
for i in aa:
    print(n,i)
    n+=1
    if not is_start:
        if len(i.strip())>0:
            is_start=True
            v=i.strip().split(' ')
            d['method']=v[0]
            d['url']=v[1]
    else:
        if  is_body:
            d['body']+=i
        elif  len(i.strip())>0:
            try:
                vv=i.split(': ')
                d['headers'][str(vv[0])]=str(vv[1])
            except :
                pass
        else:
            is_body=True
print(d)


    
