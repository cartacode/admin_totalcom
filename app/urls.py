# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path
from app import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('upload_domains/<int:user_id>', views.upload_domains_to_user,
    		name="upload_domains"),
]
