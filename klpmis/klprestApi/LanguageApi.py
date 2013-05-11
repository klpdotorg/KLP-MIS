#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
LanguageApi is used to create new language 
"""

from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry


class KLP_Language(Collection):

    """ To create new language language/creator/"""

    def get_entry(self, language_id):
        language = Moi_Type.objects.all(id=language_id)
        return ChoiceEntry(self, language)


def KLP_Language_Create(request):
    """ To Create new language language/creator/"""

    buttonType = request.POST.get('form-buttonType')

        # Moi_Type.objects.all()

    KLP_Language_Create = \
        KLP_Language(queryset=Moi_Type.objects.filter(pk=0),
                     permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(template_dir='viewtemplates'
                     , template_object_name='Language',
                     extra_context={'buttonType': buttonType}),
                     receiver=XMLReceiver())
    response = KLP_Language_Create.responder.create_form(request,
            form_class=Moi_Type_Form)

    return HttpResponse(response)


urlpatterns = patterns('', url(r'^language/creator/?$',
                       KLP_Language_Create))
