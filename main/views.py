from django.shortcuts import render

def index(request):
    context = {
        "naver": 0,
    }
    return render(request, 'main/index_runcoding.html', context)


