from django.urls import path
from . import views

app_name = 'mensagens'

urlpatterns = [
    path('', views.caixa_entrada, name='caixa_entrada'),
    path('conversa/<int:user_id>/', views.conversa, name='conversa'),
]