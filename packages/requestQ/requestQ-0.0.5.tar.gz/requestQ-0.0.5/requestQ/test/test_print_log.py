from requestQ import item as it,fetch,DoRequest
d=DoRequest()
it('test1',fetch("https://paytest.ciicsh.com/auth/authenticate/login", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://paytest.ciicsh.com/login?redirect=%2FtimeManagement%2FcompanyStatistics",
  "referrerPolicy": "no-referrer-when-downgrade",
  "body": "{\"userId\":\"13800920000\",\"password\":\"AAAaaa111\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "omit"
})).run(d).print_log()