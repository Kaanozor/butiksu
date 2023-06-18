# views.py da göstermiş olduğum index sayfasının path'ini burada belirtiyorum:
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('basket/', basket, name='basket'),
    path('payment/', payment, name='payment'),
    path('success/', success, name='success'),
    path('fail/', fail, name='failure'),
    path('result/', result, name='result'),
]