# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path
from core import views


urlpatterns = [
    path('', views.index),
    path('signup/', views.auth_signup, name="auth_signup"),
    path('login/', views.auth_login, name="auth_login"),
]
