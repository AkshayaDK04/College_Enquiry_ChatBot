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
]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)