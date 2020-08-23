
from django.conf.urls import url
from . import views

urlpatterns = [
     url('run_login', views.login_page),
     url('', views.index),
]

