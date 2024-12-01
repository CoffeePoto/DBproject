from django.contrib import admin
from .models import Effectiveness, MemberInfo, Menu, OrderBasket, OrderInfo

# Register your models here.
admin.site.register(Effectiveness)
admin.site.register(MemberInfo)
admin.site.register(Menu)
admin.site.register(OrderBasket)
admin.site.register(OrderInfo)