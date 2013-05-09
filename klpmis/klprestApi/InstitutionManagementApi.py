#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
InstitutionManagementApi is used to create new Institution Management
"""

from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry


class KLP_Institution_Management(Collection):

    """ To create new management institution-management/creator/"""

    def get_entry(self, institution_management_id):
        institution_management = \
            Institution_Management.objects.all(id=management_id)
        return ChoiceEntry(self, institution_management)


def KLP_Institution_Management_Create(request):
    """ To Create new institution management institution-management/creator/"""

    buttonType = request.POST.get('form-buttonType')

        # before Institution_Mangement.objects.all()

    KLP_Institution_Management_Create = \
        KLP_Institution_Management(queryset=Institution_Management.objects.filter(pk=0),
                                   permitted_methods=('GET', 'POST'),
                                   responder=TemplateResponder(template_dir='viewtemplates'
                                   ,
                                   template_object_name='InstitutionManagement'
                                   ,
                                   extra_context={'buttonType': buttonType}),
                                   receiver=XMLReceiver())
    response = \
        KLP_Institution_Management_Create.responder.create_form(request,
            form_class=Institution_Management_Form)

    return HttpResponse(response)


urlpatterns = patterns('', url(r'^institution-management/creator/?$',
                       KLP_Institution_Management_Create))
