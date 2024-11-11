# binance_tracker/urls.py

from django.urls import path
from .views import get_candles

urlpatterns = [
    path('get-candles/', get_candles, name='get_candles'),

]
