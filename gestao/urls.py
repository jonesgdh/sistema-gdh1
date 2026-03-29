from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

path('login/', auth_views.LoginView.as_view(template_name='tarefas/login.html'), name='login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('tarefas.urls', 'tarefas'), namespace='tarefas')),
    path('login/', auth_views.LoginView.as_view(template_name='tarefas/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

