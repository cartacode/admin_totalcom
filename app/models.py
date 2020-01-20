# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from core.models import BaseUser

# Create your models here.
class UserGroup(models.Model):
    user = models.ForeignKey(BaseUser,
                            null=True,
                            on_delete=models.SET_NULL,
                            related_name="usergroup_user")
    allowed_list = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "{}-{}".format(self.pk, self.user)