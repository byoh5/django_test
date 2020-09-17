from django.core.mail import EmailMessage
from django.shortcuts import render

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400


# smtp 버전 안정성 하
def sendEmail(to, subject, message):
    subject = subject
    message = message
    mail = EmailMessage(subject, message, to=[to])
    mail.send()
    return HTTP_200_OK

def contact_email(request):
    email = request.POST['email']
    text = email + request.POST['text']

    sendEmail("runcoding@naver.com", email, text)
    return render(request, 'main/index_runcoding.html')