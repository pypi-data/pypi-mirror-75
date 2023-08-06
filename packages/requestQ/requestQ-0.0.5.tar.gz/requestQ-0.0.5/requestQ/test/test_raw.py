from requestQ import item , raw,Case
a=item('test1',raw(
'''
GET https://paytest.ciicsh.com/business/companyDepartment/orgInfo?orgTree=true&companyId=company_000764 HTTP/1.1
Host: paytest.ciicsh.com
Connection: keep-alive
Accept: application/json, text/plain, */*
timestamp: 1596532992254
signStr: 06d469221a4a9b3aab41d686120cc491
tenant_id: tenant_021265
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnRJZCI6InRlbmFudF8wMjEyNjUiLCJsb2dpblRva2VuIjoiM2I5OTMzNzUtMzU4Mi00NzgxLWFmZjgtZmMzZjc1NDgzNmMwIiwidXNlcklkIjoiMTM4MDA5MjAwMDAifQ.4olYnVkvRhq3yPbjSXBfDmGh2TEFubJFLRcmTh-xFlY
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://paytest.ciicsh.com/employee/list
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=8DEFAC5E90EEBC91C33AA744798114B2; Login_Token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnRJZCI6InRlbmFudF8wMjEyNjUiLCJsb2dpblRva2VuIjoiM2I5OTMzNzUtMzU4Mi00NzgxLWFmZjgtZmMzZjc1NDgzNmMwIiwidXNlcklkIjoiMTM4MDA5MjAwMDAifQ.4olYnVkvRhq3yPbjSXBfDmGh2TEFubJFLRcmTh-xFlY

'''
)).expect('data.code').toBe(0)
Case('t',a).run(True)