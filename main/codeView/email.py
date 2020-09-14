from django.core.mail import EmailMessage
from django.shortcuts import render

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400

# smtp 버전 안정성 하
def MailView(request):
    # def post(self, request, format=None):
    #     email = request.data['email']
    email = "oneppp1019@naver.com"
    if email is not None:
        subject = 'Django를 통해 발송된 메일입니다.'
        message = 'Google SMTP에서 발송되었습니다.'
        mail = EmailMessage(subject, message, to=[email])
        mail.send()
        return HttpResponse(HTTP_200_OK)
    else:
        return HttpResponse(HTTP_400_BAD_REQUEST)

def sendEmail(to, subject, message):
    subject = subject
    message = message
    mail = EmailMessage(subject, message, to=[to])
    mail.send()
    return HTTP_200_OK

def contact_email(request):
    email = request.POST['email']
    text = request.POST['text']

    sendEmail("runcoding@naver.com", email, text)
    return render(request, 'main/index_runcoding.html')