from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render
from django.http import HttpResponse
from main.query import select_register
from main.codeView.comunity import *
from main.codeView.main import *

import string
import random
import bcrypt

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400

message_ok = 200
message_diff_pass = 202
message_no_regi = 204
message_exist_id = 208

# smtp 버전 안정성 하

def sendEmailWithHtml(to, subject, html_content):

    text_content = ''
    msg = EmailMultiAlternatives(subject, text_content, '', [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HTTP_200_OK

def sendEmail(to, subject, message):
    subject = subject
    message = message
    mail = EmailMessage(subject, message, to=[to])
    mail.send()
    return HTTP_200_OK

def contact_email(request):
    email = request.POST['email']
    text = request.POST['text']

    subject = "[b2b] " + email

    sendEmail("runcoding@naver.com", subject, text)
    return main_page(request)

def info_email(request):
    email = request.POST['email']
    text = request.POST['text']

    subject = "[info] " + email

    sendEmail("runcoding@naver.com", subject, text)
    return comunity_page(request)

def find_pass_viaEmail(request):
    if request.method == "POST":
        find_loginId = request.POST['find_loginId']
        regi_info = select_register(find_loginId) # 가입자 인지 확인
        if regi_info.count() is 0:
            return HttpResponse(message_no_regi)
        else:
            string_pool = string.ascii_letters
            number_pool = string.digits
            _LENGTH = 6
            newPW = ""
            for i in range(_LENGTH):
                if i == 2 or i == 5:
                    newPW += random.choice(number_pool)
                else:
                    newPW += random.choice(string_pool)  # 랜덤한 문자열 하나 선택

            new_user = regi_info[0]
            password_encrypt = bcrypt.hashpw(newPW.encode('utf-8'), bcrypt.gensalt())
            new_user.regi_pass = password_encrypt.decode('utf-8')
            new_user.save()

            html_content = '안녕하세요. 런코딩 입니다. <br/><br/>' \
                           '임시로 발급된 비밀번호는 <strong>[' + newPW + ']</strong> 입니다. <br/> ' \
                           '로그인 후, 비밀번호를 다시 설정해 주세요. <br /><br /> 런코딩 드림.<br />'

            result = sendEmailWithHtml(find_loginId, '런코딩에서 임시 비밀번호를 발송해 드렸습니다.', html_content)
            if result == 200:
                return HttpResponse(message_ok)

