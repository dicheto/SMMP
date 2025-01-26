from django.urls import path
from . import views



urlpatterns = [
    path('dashboard/' , views.dashboard, name = 'dashboard'),
    path('login/', views.log_in, name = 'login'),
    path('signin/', views.sign_in, name = 'signin'),
    path('logout' , views.logout, name = 'logout'),
    path('chooseGeneration/', views.chooseGeneration, name= 'chooseGeneration'),
]
