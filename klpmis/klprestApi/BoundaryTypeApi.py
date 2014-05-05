#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BoundaryTypeApi is used to create new boundary type
"""

from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry


class BoundaryTypeView(Collection):

    """ To Create New Boundary Type boundary-type/creator/"""

    def get_entry(self, boundary_type_id):
        boundary_type = Boundary_Type.objects.all(id=boundary_type_id)
        return ChoiceEntry(self, boundary_type)


# before Boundary_Type.objects.all()

template_boundary_type_view = \
    BoundaryTypeView(queryset=Boundary_Type.objects.filter(pk=0),
                     permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(template_dir='viewtemplates'
                     , template_object_name='boundary_type'),
                     receiver=XMLReceiver())

urlpatterns = patterns('', url(r'^boundary-type/creator/?$',
                       template_boundary_type_view.responder.create_form,
                       {'form_class': 'boundary_type'}))
