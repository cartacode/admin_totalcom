# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path
from app import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('domains/', views.domains, name="domains"),
    path('upload_domains/<int:user_id>/', views.upload_domains_to_user,
        name="upload_domains"),
    path('<str:domain>/stats/', views.domain_stats,
        name="domain-stats"),
    path('<str:domain>/events/', views.events_page,
        name="events"),
    path('<str:domain>/events/<str:begin>/<str:end>', views.domain_events,
        name="events-range"),
    path('users/', views.users, name="users"),
    # path('reports/', views.report, name="reports"),
]
