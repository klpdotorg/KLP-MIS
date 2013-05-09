#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Data format classes ("responders") that can be plugged 
into model_resource.ModelResource and determine how
the objects of a ModelResource instance are rendered
(e.g. serialized to XML, rendered by templates, ...).
"""

from django.core import serializers
from django.core.handlers.wsgi import STATUS_CODE_TEXT
from django.core.paginator import QuerySetPaginator, InvalidPage

# the correct paginator for Model objects is the QuerySetPaginator,
# not the Paginator! (see Django doc)

from django.core.xheaders import populate_xheaders
from django import forms
from django.http import Http404, HttpResponse
from django.forms.util import ErrorDict
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
import  simplejson
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.generic import TemplateView
import json
from schools.models import StudentGroup, Answer, \
    Student_StudentGroupRelation


class TreeSerializeResponder(object):

    """
    Class for all data formats that are possible
    with Django's serializer framework.
    """

    def __init__(
        self,
        CDict,
        format,
        mimetype=None,
        paginate_by=None,
        allow_empty=False,
        ):
        """
        format:
            may be every format that works with Django's serializer
            framework. By default: xml, python, json, (yaml).
        mimetype:
            if the default None is not changed, any HttpResponse calls 
            use settings.DEFAULT_CONTENT_TYPE and settings.DEFAULT_CHARSET
        paginate_by:
            Number of elements per page. Default: All elements.
        """

        self.format = format
        self.mimetype = mimetype
        self.paginate_by = paginate_by
        self.allow_empty = allow_empty
        self.expose_fields = []
        self.CDict = CDict

    def render(self, object_list):
        """
        Serializes a queryset to the format specified in
        self.format.
        """

        # Hide unexposed fields

        hidden_fields = []

        for obj in list(object_list):
            for field in obj._meta.fields:
                if not field.name in self.expose_fields \
                    and field.serialize:
                    field.serialize = False
                    hidden_fields.append(field)

        response = serializers.serialize(self.format, object_list)

        # Show unexposed fields again

        response1 = serializers.serialize(self.format, object_list,
                use_natural_keys=True)
        response1 = simplejson.loads(response)
        response2 = []
        
        for index,k in enumerate(response1):

            modelName = k['model'].split('.')[-1]
            childkey = modelName + '_' + str(k['pk'])
            temval = self.CDict[childkey]
        
            if temval:
                childval = temval[0]
                if type(childval)() == []:
                    childval = childval[0]

                    for index,c in enumerate(temval):
                        copyk = k.copy()
                        if childval:

                                          # if object has childval(has child objects) pass haschildren true

                            copyk['hasChildren'] = 'true'
                        copyk['id'] = childkey+'_'+str(index)
                        names = copyk['fields']

                                     # get names of object to show in tree structure

                        try:
                            titleval = names['name']
                        except:
                            titleval = names['question']
                        copyk['text'] = c[1]

                        response2.append(copyk)
                        del copyk
                    response1 = response2
                else:
                    if childval:

                          # if object has childval(has child objects) pass haschildren true

                        k['hasChildren'] = 'true'
                    k['id'] = childkey
                    names = k['fields']

                # get names of object to show in tree structure

                    try:
                        titleval = names['name']
                    except:
                        titleval = names['question']
                    k['text'] = temval[1]

        response = simplejson.dumps(response1)
        for field in hidden_fields:
            field.serialize = True
        return response

    def element(self, request, elem):
        """
        Renders single model objects to HttpResponse.
        """

        return HttpResponse(self.render([elem]), self.mimetype)

    def error(
        self,
        request,
        status_code,
        error_dict=None,
        ):
        """
        Handles errors in a RESTful way.
        - appropriate status code
        - appropriate mimetype
        - human-readable error message
        """

        if not error_dict:
            error_dict = ErrorDict()
        response = HttpResponse(mimetype=self.mimetype)
        response.write('%d %s' % (status_code,
                       STATUS_CODE_TEXT[status_code]))
        if error_dict:
            response.write('''

Errors:
''')
            response.write(error_dict.as_text())
        response.status_code = status_code
        return response

    def list(
        self,
        request,
        queryset,
        page=None,
        ):
        """
        Renders a list of model objects to HttpResponse.
        """

        if self.paginate_by:
            paginator = QuerySetPaginator(queryset, self.paginate_by)
            if not page:
                page = request.GET.get('page', 1)
            try:
                page = int(page)
                object_list = paginator.page(page).object_list
            except (InvalidPage, ValueError):
                if page == 1 and self.allow_empty:
                    object_list = []
                else:
                    return self.error(request, 404)
        else:
            object_list = list(queryset)
        return HttpResponse(self.render(object_list), self.mimetype)


class TreeResponder(TreeSerializeResponder):

    """
    JSON data format class.
    """

    def __init__(
        self,
        CDict,
        paginate_by=None,
        allow_empty=False,
        ):
        TreeSerializeResponder.__init__(
            self,
            CDict,
            'json',
            'application/json',
            paginate_by=paginate_by,
            allow_empty=allow_empty,
            )

    def error(
        self,
        request,
        status_code,
        error_dict=None,
        ):
        """
        Return JSON error response that includes a human readable error
        message, application-specific errors and a machine readable
        status code.
        """

        if not error_dict:
            error_dict = ErrorDict()
        response = HttpResponse(mimetype=self.mimetype)
        response.status_code = status_code
        response_dict = {'error-message': '%d %s' % (status_code,
                         STATUS_CODE_TEXT[status_code]),
                         'status-code': status_code,
                         'model-errors': error_dict.as_ul()}
        simplejson.dump(response_dict, response)
        return response


