#-*- coding: utf-8 -*-
import requests
import json
import base64
from django.http import HttpResponse
# 운영
# url = 'https://api.bizppurio.com/'
# 검수
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

url = 'https://dev-api.bizppurio.com'

tokenUrl = url + '/v1/token'
msgUrl = url + '/v3/message'
imgFileUrl = url + '/v1/file'
responseRereq = url + '/v2/report'


#
# data = {
#  'account': 'test',
#  'refkey': '1234',
#  'type': 'at',
#  'from': '07000000000',
#  'to': '01000000000',
#  'content': {
#  'at': {
#  'senderkey': '123',
#  'templatecode': '1234',
#  'message': '알림톡',
#  'button': [
#  {
#  'name': '확인하러 가기',
#  'type': 'WL',
#  'url_mobile': 'http://www.daou.com',
#  'url_pc': 'http://www.daou.com'
#  }
#  ]
#  }
#  }
# }

# headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Authorization": "{인증 토큰}"}
# response = session.post(url, data=json.dumps(data), headers=headers)
# print("Status code: ", response.status_code)
# print("Printing Entire Post Request")
# print(response.json())

def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))


def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')


# getToken
def get_token(request):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    user = "runcoding_biz:run!coding4"
    b64Val = stringToBase64(user)

    print("auth encode 64")
    print(b64Val)

    session = requests.Session()
    # 운영인 경우, verify 속성을 True 로 변경
    # session.verify = True
    session.verify = False
    headers = {'Authorization': 'Basic %s' % b64Val, 'Content-Type': 'application/json; charset=utf-8'}

    token_msg = session.post(tokenUrl,  headers=headers)
    res_code = token_msg.status_code
    print(res_code)
    print(token_msg.json())
    print(token_msg.request.headers)
    # json_msg = token_msg.json()
    # json_res = json_msg["response"]
    # access_token = json_res["accesstoken"]

    # print(json_msg)
    # print(access_token)

    return HttpResponse(res_code)
