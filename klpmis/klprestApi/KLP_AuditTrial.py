#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
KLP_AuditTrial is used to generate audit trail report using fullhistory.
"""

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_restapi.responder import *
from django_restapi.receiver import *
from schools.models import *

from schools.receivers import KLP_user_Perm
from fullhistory.models import FullHistory
from django.db.models import Q
import datetime
from django.contrib.contenttypes.models import ContentType


def KLP_audit(request):
    """ This method is used to show audit trail report for the users using fullhistory """

    user = request.user  # get logged in user

    # check user permissions to access audit trial report

    KLP_user_Perm(request.user, 'Audit', None)

    # get all active(1) user to show in drop down.

    userList = User.objects.filter(is_active=1)
    respDict = {'userList': userList,
                'title': 'Karanataka Learning Partnership'}

    # check requested method

    if request.POST:

        # if request methos is post get selcted user from drop down

        selUser = request.POST.get('selUser')
        today = datetime.date.today()
        defaultDate = today.strftime('%d') + '-' + today.strftime('%m') \
            + '-' + today.strftime('%Y')

        # get start date and end date

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # if start date and end date are empty then default start date and end date are current date.

        if not start_date:
            start_date = defaultDate
        if not end_date:
            end_date = defaultDate
        respDict['start_date'] = start_date
        respDict['end_date'] = end_date
        respDict['selUser'] = int(selUser)
        strDate = start_date.split('-')
        enDate = end_date.split('-')

        # Query fullhistory table based on start date, end date and selected user

        fullHistoryList = \
            FullHistory.objects.filter(action_time__range=(datetime.date(int(strDate[2]),
                int(strDate[1]), int(strDate[0])),
                datetime.date(int(enDate[2]), int(enDate[1]),
                int(enDate[0]))), request__user_pk=selUser)
        respDict['fullHistoryList'] = fullHistoryList

        # return reponse to template

        return render_to_response('viewtemplates/auditTrial.html',
                                  respDict,
                                  context_instance=RequestContext(request))
    return render_to_response('viewtemplates/auditTrial.html',
                              respDict,
                              context_instance=RequestContext(request))


urlpatterns = patterns('', url(r'^audit/trial/$', KLP_audit))
