from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: redirect('mainpage_before/')),
    path('mainpage_before/', views.mainpage_before, name='mainpage_before'),
    path('mainpage_after/', views.mainpage_after, name='mainpage_after'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('detail/', views.detail, name='detail'),
    path('cart/', views.cart, name='cart'),
    path('addcart/', views.addcart, name='addcart'),
    path('order/', views.order, name='order'),
]
