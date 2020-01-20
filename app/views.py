# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests
import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import BaseUser
from app.models import UserGroup

MAILGUN_API = "https://api.mailgun.net/v3"

# Create your views here.
@login_required
def dashboard(request):
    context = {}
    domains = []
    allowed_list = None

    user_group = UserGroup.objects.filter(
            user=request.user).values("allowed_list")
    if allowed_list:
        allowed_list = user_group[0]["allowed_list"].split(",")
        context["allowed_list"] = allowed_list

    try:
        res = requests.get("{}/domains".format(MAILGUN_API),
                            auth=("api", settings.MAINGUN_KEY))
        response_body = json.loads(res.text)
        if hasattr(response_body, "items"):
            domains = response_body["items"]
    except Exception as e:
        context['error'] = str(e)
        print("@@@@ eeror @@@: ", str(e))
        return render(request, "app/dashboard.html", context)

    print(len(domains))
    if allowed_list:
        allowed_domains = list(filter(lambda d: d["name"] in context, domains))
    else:
        allowed_domains = domains
    context["allowed_domains"] = domains
    return render(request, "app/dashboard.html", context)

@csrf_exempt
def upload_domains_to_user(request, user_id):
    context = dict()

    if request.method != "POST":
        context["error"] = "User id doesn't exist!"
        return JsonResponse(context)
    else:
        try:
            user = BaseUser.objects.get(id=user_id)
        except:
            context["error"] = "User id doesn't exist!"
            return JsonResponse(context)

        body = json.loads(request.body)
        domains = body["domains"] if "domains" in body else None

        obj, created = UserGroup.objects.get_or_create(user=user,
                                allowed_list=domains)
        
        context["msg"] = "Success!"
        return JsonResponse(context)

def domain_stats(request, domain):
    context = {}
    try:
        res = requests.get(
            "{}/{}/stats/total".format(MAILGUN_API, domain),
            auth=("api", settings.MAINGUN_KEY),
            params={"event": ["accepted", "delivered", "failed"],
                    "duration": "1h"})
        response_body = json.loads(res.text)
        print(response_body)
        if "stats" in response_body:
            context['stats'] = json.dumps(response_body)
        else:
            context['error'] = "no response"
    except Exception as e:
        context['error'] = str(e)
    print(context)
    return render(request, 'app/stats.html', context)


def domain_stats(request, domain):
    context = {}
    try:
        res = requests.get(
            "{}/{}/events".format(MAILGUN_API, domain),
            auth=("api", settings.MAINGUN_KEY))
        response_body = json.loads(res.text)

        context['stats'] = json.dumps(response_body)
        # if "stats" in response_body:
        # else:
        #     context['error'] = "no response"
    except Exception as e:
        context['error'] = str(e)
    print(context)
    return render(request, 'app/events.html', context)



