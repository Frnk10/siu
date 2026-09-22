from django.urls import path
from Aplicaciones.user.api import *
urlpatterns = [
    path('usuarios/', user_view, name='user_list'),
    path('usuarios/<int:pk>/', user_detail, name='user_detail'),
]