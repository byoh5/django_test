from django.http import HttpResponse

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400

def watch_esp_cam(request):
    data = request.GET.get('data', '0')
    esp32_num = request.GET.get('esp32_num', '0')

    print(data, esp32_num)

    return HttpResponse(HTTP_200_OK)
