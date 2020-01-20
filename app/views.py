# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import BaseUser
from app.models import UserGroup

# Create your views here.
@login_required
def dashboard(request):
	return render(request, "app/dashboard.html")

@csrf_exempt
def upload_domains_to_user(request, user_id):
	context = dict()
	print(user_id, request.POST)
	if request.method != "POST":
		context["error"] = "User id doesn't exist!"
		return JsonResponse(context)
	else:
		try:
			user = BaseUser.objects.get(id=user_id)
		except:
			context["error"] = "User id doesn't exist!"
			return JsonResponse(context)

		domains = request.POST.get("domains", None)
		obj, created = UserGroup.objects.get_or_create(user=user,
								allowed_list=domains)
		
		context["msg"] = "Success!"
		return JsonResponse(context)



