from aiogram.methods import send_message
from django.urls import path
from .views import *


urlpatterns = [
    path('chat/', get_chat, name='new_chat'),
    path('qr/', get_qr, name='qr_code'),
    path('remove_chat/', remove_chat, name='remove_chat'),
    path('status/', get_status, name='get_status'),
    path('send_message', send_message, name='send_message'),
]
