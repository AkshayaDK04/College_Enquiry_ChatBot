from django.contrib import admin
from django.urls import path
from . import   views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    path('chatbot/',views.chatbots,name='chatbot'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('signout/', views.signout, name='signout'),
]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)