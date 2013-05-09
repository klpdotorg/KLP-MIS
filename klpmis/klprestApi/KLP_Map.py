#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry
from django.template import Template, Context, RequestContext
from schools.models import *


def KLP_Map_SG(request):
    """ This method uses to map Student Groups With Assessment"""

    boundary_id = request.GET.get('boundary')
    asssessment_id = request.GET.get('assessment')
    assessmentObj = Assessment.objects.get(id=asssessment_id)
    studentgroup_list = \
        StudentGroup.objects.filter(institution__boundary__parent__parent__id=boundary_id)
    for sg in studentgroup_list:
        sg_as_mapObj = \
            Assessment_StudentGroup_Association(assessment=assessmentObj,
                student_group=sg, active=2)
        sg_as_mapObj.save()
    return HttpResponse(studentgroup_list)


urlpatterns = patterns('', url(r'^map/sg/as/$', KLP_Map_SG))

