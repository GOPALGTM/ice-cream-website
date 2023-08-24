from unicodedata import name
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path("",views.index, name='index'),
    path("about/",views.about, name='about'),
    path("services/",views.services, name='services'),
    path("contact/",views.contact, name='contact'),
    path('login/',views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout_view, name='logout'),
    path('forgot_password/', views.send_reset_password_email, name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
]
