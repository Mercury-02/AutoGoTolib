import http
import requests
import urllib
import time

def preheader(content_length, cookie_string):
    header = {
        'Host': 'wechat.v2.traceint.com',
        'Connection': 'keep-alive',
        'Content-Length': content_length,
        'App-Version': '2.1.2.p1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/9105 Flue',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://web.traceint.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://web.traceint.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie':
            'FROM_TYPE=weixin; v=5.5;'
            'wechatSESS_ID=4bf28879c2087f37c1fe1caf3514d70661054c9f21ec9ffe;'
            + cookie_string
    }
    return header
def get_code(url):
    query = urllib.parse.urlparse(url).query
    codes = urllib.parse.parse_qs(query).get('code')
    if codes:
        return codes.pop()
    else:
        raise ValueError("Code not found in URL")
def get_cookie_string(code):
    cookiejar = http.cookiejar.MozillaCookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
    response = opener.open(
        "http://wechat.v2.traceint.com/index.php/urlNew/auth.html?" + urllib.parse.urlencode({
            "r": "https://web.traceint.co"
                 "m/web/index.html",
            "code": code,
            "state": 1
        })
    )
    cookie_items = []
    for cookie in cookiejar:
        cookie_items.append(f"{cookie.name}={cookie.value}")
    cookie_string = '; '.join(cookie_items)
    return cookie_string
def replace_cookie_string(new_cookies, cookie_string):
    for cookie in new_cookies:
        if cookie.name == 'Authorization':
            cookie_string = cookie_string.replace(cookie_string.split(';')[0], 'Authorization=' + cookie.value)
        elif cookie.name == 'SERVERID':
            cookie_string = cookie_string.replace(cookie_string.split(';')[2],'SERVERID=' + cookie.value)
            cookie_string = cookie_string.replace(cookie_string.split(';')[1], ' SERVERID=' + cookie.value)
    return cookie_string
def post_main(cookie_string):
    header = preheader('1172', cookie_string)
    url = "http://wechat.v2.traceint.com/index.php/graphql/"
    data = \
        {"operationName": "index",
         "query": "query index($pos: String!, $param: [hash]) {\n userAuth {\n oftenseat {\n list {\n id\n info\n lib_id\n seat_key\n status\n }\n }\n message {\n new(from: \"system\") {\n has\n from_user\n title\n num\n }\n indexMsg {\n message_id\n title\n content\n isread\n isused\n from_user\n create_time\n }\n }\n reserve {\n reserve {\n token\n status\n user_id\n user_nick\n sch_name\n lib_id\n lib_name\n lib_floor\n seat_key\n seat_name\n date\n exp_date\n exp_date_str\n validate_date\n hold_date\n diff\n diff_str\n mark_source\n isRecordUser\n isChooseSeat\n isRecord\n mistakeNum\n openTime\n threshold\n daynum\n mistakeNum\n closeTime\n timerange\n forbidQrValid\n renewTimeNext\n forbidRenewTime\n forbidWechatCancle\n }\n getSToken\n }\n currentUser {\n user_id\n user_nick\n user_mobile\n user_sex\n user_sch_id\n user_sch\n user_last_login\n user_avatar(size: MIDDLE)\n user_adate\n user_student_no\n user_student_name\n area_name\n user_deny {\n deny_deadline\n }\n sch {\n sch_id\n sch_name\n activityUrl\n isShowCommon\n isBusy\n }\n }\n }\n ad(pos: $pos, param: $param) {\n name\n pic\n url\n }\n}",
         "variables": {"pos": "App-首页"}}
    session = requests.session()
    current_time = time.strftime("%H:%M:%S", time.localtime())
    res = session.post(url=url, headers=header, json=data)
    new_cookies = res.cookies
    print(res.text, "\n", current_time, 'post_main done')
    return new_cookies
def getuserCancelConfig(cookie_string):
    header = preheader('194',cookie_string)
    url = 'http://wechat.v2.traceint.com/index.php/graphql/'
    data= \
    {"operationName": "getUserCancleConfig",
     "query": "query getUserCancleConfig {\n userAuth {\n user {\n holdValidate: getSchConfig(fields: \"hold_validate\", extra: true)\n }\n }\n}",
     "variables": {}
     }
    req = requests.post(url=url, headers=header, json=data)
    print('getuserCancelConfig done',req.text)
def list(cookie_string):
    header = preheader('729',cookie_string)
    url = 'http://wechat.v2.traceint.com/index.php/graphql/'
    data = \
        {"operationName":"list",
         "query":"query list {\n userAuth {\n reserve {\n libs(libType: -1) {\n lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n lib_group_id\n lib_comment\n lib_rt {\n seats_total\n seats_used\n seats_booking\n seats_has\n reserve_ttl\n open_time\n open_time_str\n close_time\n close_time_str\n advance_booking\n }\n }\n libGroups {\n id\n group_name\n }\n reserve {\n isRecordUser\n }\n }\n record {\n libs {\n lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n lib_group_id\n lib_comment\n lib_color_name\n lib_rt {\n seats_total\n seats_used\n seats_booking\n seats_has\n reserve_ttl\n open_time\n open_time_str\n close_time\n close_time_str\n advance_booking\n }\n }\n }\n rule {\n signRule\n }\n }\n}"
         }
    res = requests.post(url=url, headers=header, json=data)
    print('list done',res.text)
def liblayout(cookie_string,libId=413):
    header = preheader('390',cookie_string)
    url = 'http://wechat.v2.traceint.com/index.php/graphql/'
    data = \
        {"operationName": "libLayout",
         "query": "query libLayout($libId: Int, $libType: Int) {\n userAuth {\n reserve {\n libs(libType: $libType, libId: $libId) {\n lib_id\n is_open\n lib_floor\n lib_name\n lib_type\n lib_layout {\n seats_total\n seats_booking\n seats_used\n max_x\n max_y\n seats {\n x\n y\n key\n type\n name\n seat_status\n status\n }\n }\n }\n }\n }\n}",
         "variables": {"libId": libId}
         }
    res = requests.post(url=url, headers=header, json=data)
    print('liblayout done',res.text)
def reserue(cookie_string,seatKey="12,7",libId=413):
    header = preheader('350',cookie_string)
    url = 'http://wechat.v2.traceint.com/index.php/graphql/'
    data = \
        {"operationName":"reserueSeat",
         "query":"mutation reserueSeat($libId: Int!, $seatKey: String!, $captchaCode: String, $captcha: String!) {\n userAuth {\n reserve {\n reserueSeat(\n libId: $libId\n seatKey: $seatKey\n captchaCode: $captchaCode\n captcha: $captcha\n )\n }\n }\n}",
         "variables":{"seatKey":seatKey,"libId":libId,"captchaCode":"","captcha":""}
         }
    res = requests.post(url=url, headers=header, json=data)
    print('reserve done',res.text)

if __name__ == '__main__':
    url = input("Please input the url:")
    code = get_code(url)
    cookie_string = get_cookie_string(code)
    print(cookie_string,'first cookie_string')
    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if current_time < '05:59:00' or current_time > '06:00:05':
            new_cookie = post_main(cookie_string)
            cookie_string = replace_cookie_string(new_cookie, cookie_string)
            time.sleep(60)
            print(cookie_string)
        elif '05:59:00' <= current_time < '06:00:00':
            print(f'waiting for the time,{current_time}')
            time.sleep(1)
        elif '06:00:00' <= current_time <= '06:00:05':
            getuserCancelConfig(cookie_string)
            list(cookie_string)
            liblayout(cookie_string)
            reserue(cookie_string)
            time.sleep(1)
            print(f'completely done,{current_time}')