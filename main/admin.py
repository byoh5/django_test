from django.contrib import admin
from main.models import RegisterTB
from main.models import LoginTB
from main.models import PrdTB
from main.models import ItemTB
from main.models import OrderTB
# Register your models here.

admin.site.register(RegisterTB)
admin.site.register(LoginTB)
admin.site.register(PrdTB)
admin.site.register(ItemTB)
admin.site.register(OrderTB)