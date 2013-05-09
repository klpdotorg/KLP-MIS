#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ProgrammeApi is used 
1) To view Individual Programme details.
2) To create new Programme
3) To update existing Programme
4) To list Programmes onchange of boundary type in filterbyprogramme link.
"""

from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry
import datetime

from schools.receivers import KLP_user_Perm


class KLP_Programme(Collection):

    def get_entry(self, programme_id):

        # Query For Programme

        programme = Programme.objects.get(id=programme_id)
        return ChoiceEntry(self, programme)


def KLP_Programme_View(request, programme_id):
    """ To View Selected Programme programme/(?P<programme_id>\d+)/view/"""

    kwrg = {'is_entry': True}

        # before Programme.objects.all()

    resp = \
        KLP_Programme(queryset=Programme.objects.filter(pk=programme_id),
                      permitted_methods=('GET', 'POST'),
                      responder=TemplateResponder(template_dir='viewtemplates'
                      , template_object_name='programme'))(request,
            programme_id, **kwrg)
    return HttpResponse(resp)


def KLP_Programme_Create(request):
    """ To Create New Programme programme/creator/"""

    # Checking user Permissions for programme add

    KLP_user_Perm(request.user, 'Programme', 'Add')

        # Get Current date for to pass for calendar

    now = datetime.date.today()
    buttonType = request.POST.get('form-buttonType')
    currentMont = int(now.strftime('%m'))
    endYear = int(now.strftime('%Y'))
    if currentMont > 4:
        endYear = endYear + 1

        # before Programme.objects.all()

    KLP_Create_Programme = \
        KLP_Programme(queryset=Programme.objects.filter(pk=0),
                      permitted_methods=('GET', 'POST'),
                      responder=TemplateResponder(template_dir='viewtemplates'
                      , template_object_name='programme',
                      extra_context={
        'buttonType': buttonType,
        'end_date': 30,
        'endYear': endYear,
        'endMonth': 'APRIL',
        }), receiver=XMLReceiver())
    response = KLP_Create_Programme.responder.create_form(request,
            form_class=Programme_Form)

    return HttpResponse(response)


def KLP_Programme_Update(request, programme_id):
    """ To update Selected Programme programme/(?P<programme_id>\d+)/update/"""

    # Checking user Permissions for programme update

    KLP_user_Perm(request.user, 'Programme', 'Update')

        # Get Current date for to pass for calendar

    now = datetime.date.today()
    buttonType = request.POST.get('form-buttonType')
    currentMont = int(now.strftime('%m'))
    endYear = int(now.strftime('%Y'))
    if currentMont > 4:
        endYear = endYear + 1

        # before Programme.objects.all()

    KLP_Edit_Programme = \
        KLP_Programme(queryset=Programme.objects.filter(pk=programme_id),
                      permitted_methods=('GET', 'POST'),
                      responder=TemplateResponder(template_dir='edittemplates'
                      , template_object_name='programme',
                      extra_context={
        'buttonType': buttonType,
        'end_date': 30,
        'endYear': endYear,
        'endMonth': 'APRIL',
        }), receiver=XMLReceiver())
    response = KLP_Edit_Programme.responder.update_form(request,
            pk=programme_id, form_class=Programme_Form)

    return HttpResponse(response)


class KLP_Get_Programms(Resource):

    """ To get  programmes based on type selected filter/(?P<type_id>\d+)/programme/"""

    def read(self, request, type_id):
        try:

            # Query for active programmes based on category

            programme_list = \
                Programme.objects.filter(programme_institution_category=type_id,
                    active=2).order_by('-start_date', '-end_date', 'name'
                    ).only('id', 'name')
            respStr = ''
            for programme in programme_list:
                respStr += '%s$$%s&&' % (programme.id, programme)
            return HttpResponse(respStr[0:len(respStr) - 2])
        except:
            return HttpResponse('fail')


urlpatterns = patterns('',
                       url(r'^programme/(?P<programme_id>\d+)/view/?$',
                       KLP_Programme_View), url(r'^programme/creator/?$'
                       , KLP_Programme_Create),
                       url(r'^programme/(?P<programme_id>\d+)/update/$'
                       , KLP_Programme_Update),
                       url(r'^filter/(?P<type_id>\d+)/programms/$',
                       KLP_Get_Programms(permitted_methods=('POST',
                       'GET'))))
