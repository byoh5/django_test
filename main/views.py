from django.shortcuts import render

def index(request):
    return render(request, 'main/index_runcoding.html')

# Create your views here.
