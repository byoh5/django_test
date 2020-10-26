from django.http import HttpResponse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400

@method_decorator(csrf_exempt)
def watch_esp_cam(request):
    data = request.POST.get('data', '0')
    esp32_num = request.POST.get('esp32_num', '0')

    print(data, esp32_num)
    print(csrf.get_token(request))

    return HttpResponse(HTTP_200_OK)
