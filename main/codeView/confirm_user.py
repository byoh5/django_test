import json
import requests
from django.shortcuts import render
from main.query import *
from main.models import *
import bcrypt

response_fail = 401 # 인증된 이름이 가입자와 다름
response_ok = 200

def getConfirm(request):
    run_uid = request.POST['run_uid']
    regi_idx = request.POST['regi_idx']
    new_phone = changePhone_format(request.POST['new_phone'])

    regi_info = select_register_idx(regi_idx)
    runcoding = select_runcoding()

    key = runcoding[0].imp_key
    secret = runcoding[0].imp_secret

    # getToken
    post_data = {
                    'imp_key': key,
                    'imp_secret': secret
                }
    token_msg = requests.post(url='https://api.iamport.kr/users/getToken', data=json.dumps(post_data) , headers={'Content-Type': 'application/json'})

    json_msg = token_msg.json()
    json_res = json_msg["response"]
    access_token = json_res["access_token"]

    # get auth user info
    confirm_user_msg = requests.get(url='https://api.iamport.kr/certifications/' + run_uid, headers={'Authorization': access_token})
    json_user_msg = confirm_user_msg.json()
    json_user_msg_res = json_user_msg["response"]

    name = json_user_msg_res["name"]

    # runcoding db save
    confirm = danal_confirmTB(imp_uid=run_uid, regi_user=regi_info[0], access_token=access_token, new_phone=new_phone, imp_name=name )
    confirm.save()

    msg = response_ok
    if regi_info[0].regi_name == name:
        new_regi = regi_info[0]
        new_regi.regi_phone = confirm.new_phone
        new_regi.save()

        regi_info = select_register_idx(regi_idx)
    else:
        msg = response_fail

    context = {
        "user_detail": regi_info,
        "message": msg,
    }
    return render(request, 'mypage/myprofile.html', context)


