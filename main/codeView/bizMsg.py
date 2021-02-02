import json
from datetime import timezone
import requests, base64
from django.http import HttpResponse
# 운영
# url = 'https://api.bizppurio.com/'
# 검수
from main.query import *
from main.models import *

pay_status_ok = 1
pay_status_delivery = 2
pay_status_delivery_done = 3
pay_status_prepay = 4
pay_status_deposit_noCheck = 5


url = 'https://api.bizppurio.com'

tokenUrl = url + '/v1/token'
msgUrl = url + '/v3/message'
imgFileUrl = url + '/v1/file'
responseRereq = url + '/v2/report'

account = 'runcoding_biz'
type ='at'
template_code = 'runcoding_delevery_templete'
send_senderKey = '01460aad9f781048a1760df1d2c6ebd493dd52dc'

def get_token():
    run_info = select_runcoding()
    print(run_info[0].biz_id)

    user = str(run_info[0].biz_id) + ":" + str(run_info[0].biz_pw)
    print(user)

    b64Val = base64.b64encode(user.encode()).decode("UTF-8")

    print(b64Val)

    headers = {'Authorization': 'Basic %s' % b64Val, 'Content-Type': 'application/json; charset=utf-8'}

    token_msg = requests.post(tokenUrl,  headers=headers)
    res_code = token_msg.status_code
    json_msg = token_msg.json()

    print(res_code)
    print(json_msg)

    if res_code == 200:
        accesstoken = json_msg["accesstoken"]
        print(accesstoken)

        return accesstoken
    return 404


def send_msg_at(user, email, number, delevery_num):
    take_accesstoken = get_token()
    print(take_accesstoken)

    if take_accesstoken == 404:
       return HttpResponse(404)

    userInfo = select_pay_user_delivery(email)

    if userInfo.count() > 0:

        pay_userStatus_info = select_userStatue(pay_status_delivery)


        year = timezone.localtime().year
        month = timezone.localtime().month
        day = timezone.localtime().day

        date = str(year) + "-" + str(month) + "-" + str(day)

        post_data = {
            'account': account,
            'refkey': userInfo[0].pay_num, #주문번호
            'type': type,
            'from': '01085718372',
            'to': number,
            'content': {
                'at': {
                    'message':
                        "[런코딩]" +
                        "안녕하세요. " + user + "님\n\n" +
                        "주문하신 상품이 발송되었습니다.\n\n" +
                        "- 주문자명 : " + user + "\n" +
                        "- 날짜 : " + date + "\n" +
                        "- 상품명 : " + userInfo[0].prd_info + "\n" +
                        "- 택배사 : " + "한진택배\n" +
                        "- 운송장번호 : " + delevery_num + "\n\n" +
                        "공휴일 제외 1~2일 내에 배송될 예정입니다.\n\n",
                    'senderkey': send_senderKey,
                    'templatecode': template_code,
                    'button': [
                     {
                          "name": "런코딩",
                          "type": "WL",
                          "url_pc": "http://runcoding.co.kr",
                          "url_mobile": "http://runcoding.co.kr"
                    }]
                }
            }
        }

        headers = {'Content-Type': 'application/json; charset=utf-8', "Authorization": 'Bearer ' + take_accesstoken}

        token_msg = requests.post(url=msgUrl, data=json.dumps(post_data), headers=headers)

        res_code = token_msg.status_code
        print(res_code)
        print(token_msg.json())

        if res_code == 200:
            new_info = userInfo[0]
            new_info.pay_user_status = pay_userStatus_info[0]
            new_info.delivery_time = timezone.now()
            new_info.save()

        return HttpResponse(res_code)

    return HttpResponse(404)

