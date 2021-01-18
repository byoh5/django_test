import requests, base64
from django.http import HttpResponse
# 운영
# url = 'https://api.bizppurio.com/'
# 검수
from main.query import select_runcoding_biz

url = 'https://api.bizppurio.com'

tokenUrl = url + '/v1/token'
msgUrl = url + '/v3/message'
imgFileUrl = url + '/v1/file'
responseRereq = url + '/v2/report'

def get_token(request):

    biz_info = select_runcoding_biz()
    print(biz_info[0].biz_id)

    user = "runcoding_biz:runcoding!2"

    b64Val = base64.b64encode(user.encode()).decode("UTF-8")

    print(b64Val)

    headers = {'Authorization': 'Basic %s' % b64Val, 'Content-Type': 'application/json; charset=utf-8'}

    token_msg = requests.post(tokenUrl,  headers=headers)
    res_code = token_msg.status_code
    print(res_code)
    print(token_msg.json())

    return HttpResponse(res_code)
