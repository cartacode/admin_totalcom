# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import json
import requests
from datetime import datetime
from dateutil import parser
import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from core.models import BaseUser
from app.models import UserGroup

MAILGUN_API_URL = "https://api.mailgun.net/v3"

def mailgun_api(uri, params=None):
    if params:
        res = requests.get(
                "{}/{}".format(MAILGUN_API_URL, uri),
                auth=("api", settings.MAINGUN_KEY),
                params=params)
    else:
        res = requests.get(
                "{}/{}".format(MAILGUN_API_URL, uri),
                auth=("api", settings.MAINGUN_KEY))

    return json.loads(res.text)

def get_second_key(item):
    return item[1]


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
        res = mailgun_api("domains")
        if hasattr(res, "items"):
            domains = res["items"]
    except Exception as e:
        context['error'] = str(e)
        logger.info("line 59: {}".format(e))
        return render(request, "app/dashboard.html", context)

    if "allowed_list" in context:
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
        res = mailgun_api("{}stats/total".format(domain), 
                        {"event": ["accepted"],
                        "duration": "1h"})
        if "stats" in res:
            context['stats'] = json.dumps(res)
        else:
            context['error'] = "no response"
    except Exception as e:
        context['error'] = str(e)
        logger.info("line 104: {}".format(e))

    return render(request, 'app/stats.html', context)


def domain_events(request, domain, begin=None, end=None):
    context = {}
    recipients = []
    new_events = {}
    try:
        params = {"event": "accepted", "ascending": "yes"}
        if begin:
            params["begin"] = parser.parse(begin).timestamp()
        if end:
            params["end"] = parser.parse(end).timestamp()
        
        res = mailgun_api("{}/events".format(domain), params)
        # import pdb
        # pdb.set_trace()
        if "items" in res and len(res["items"]) > 0:
            if params["begin"] > res["items"][0]["timestamp"]:
                time.sleep(20)
                res = mailgun_api("{}/events".format(domain), params)
                if params["begin"] > res["items"][0]["timestamp"]:
                    context["error"] = "Your request may be blocked! \
                        Try again after 5 minutes."
                    return render(request, 'app/events.html', context)

            for d in res["items"]:
                hour = datetime.fromtimestamp(d["timestamp"]).hour

                if hour not in new_events:
                    new_events[hour] = 1
                else:
                    new_events[hour] = new_events[hour] + 1
            
            events = [(h, new_events[h]) for h in new_events]
            sorted(events, key=get_second_key)
            context["new_events"] = events
        else:
            context["error"] = "No result!"
            logger.info("line 146: {}".format(e))                 

    except Exception as e:
        print("line 147: {}".format(str(e)))
        context['error'] = str(e)

    return render(request, 'app/events.html', context)


def events_page(request, domain):
    context = {"domain": domain}
    if request.method == "POST":
        begin = request.POST.get("begin", None)
        end = request.POST.get("end", None)
        return redirect(reverse("domain-events", args=(domain, begin, end,)))
    return render(request, 'app/events_page.html', context)



