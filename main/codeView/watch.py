from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400

@method_decorator(csrf_exempt)
def watch_esp_cam(request):
    data = json.loads(request.body)
    print(data)

    return HttpResponse(HTTP_200_OK)
