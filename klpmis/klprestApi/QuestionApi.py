#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
QuestionApi is used 
1) To view Individual Question details.
2) To create new Question
3) To update existing Question
"""

from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from django.http import HttpResponse
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry

from schools.receivers import KLP_user_Perm


class KLP_Question(Collection):

    def get_entry(self, question_id):

        # Query For Selected Question based on question_id

        question = Question.objects.get(id=question_id)
        return ChoiceEntry(self, question)


def KLP_Question_View(request, question_id):
    """ To View Selected Question question/(?P<question_id>\d+)/view/"""

    kwrg = {'is_entry': True}

        # before Question.objects.all()

    resp = \
        KLP_Question(queryset=Question.objects.filter(pk=question_id),
                     permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(template_dir='viewtemplates'
                     , template_object_name='question'))(request,
            question_id, **kwrg)
    return HttpResponse(resp)


def KLP_Question_Create(request, referKey):
    """ To Create New Question assessment/question/(?P<referKey>\d+)/creator/"""

    # Checking user Permissions for Question add

    KLP_user_Perm(request.user, 'Question', 'Add')
    buttonType = request.POST.get('form-buttonType')  # Get Button Type

    # get number of questions under assessments for question order

    order = Question.objects.filter(assessment__id=referKey).count() + 1

        # before Question.objects.all()

    KLP_Create_Question = \
        KLP_Question(queryset=Question.objects.filter(pk=0),
                     permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(template_dir='viewtemplates'
                     , template_object_name='question',
                     extra_context={'buttonType': buttonType,
                     'referKey': referKey, 'order': order}),
                     receiver=XMLReceiver())
    response = KLP_Create_Question.responder.create_form(request,
            form_class=Question_Form)

    return HttpResponse(response)


def KLP_Question_Update(request, question_id):
    """ To update Selected Question question/(?P<question_id>\d+)/update/"""

    # Checking user Permissions for Question Update

    KLP_user_Perm(request.user, 'Question', 'Update')

        # Get Button Type

    buttonType = request.POST.get('form-buttonType')
    referKey = request.POST.get('form-0-assessment')

        # before Question.objects.all()

    KLP_Edit_Question = \
        KLP_Question(queryset=Question.objects.filter(pk=question_id),
                     permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(template_dir='edittemplates'
                     , template_object_name='question',
                     extra_context={'buttonType': buttonType,
                     'referKey': referKey}), receiver=XMLReceiver())
    response = KLP_Edit_Question.responder.update_form(request,
            pk=question_id, form_class=Question_Form)

    return HttpResponse(response)


urlpatterns = patterns('',
                       url(r'^assessment/question/(?P<referKey>\d+)/creator/?$'
                       , KLP_Question_Create),
                       url(r'^question/(?P<question_id>\d+)/view/?$',
                       KLP_Question_View),
                       url(r'^question/(?P<question_id>\d+)/update/?$',
                       KLP_Question_Update))
