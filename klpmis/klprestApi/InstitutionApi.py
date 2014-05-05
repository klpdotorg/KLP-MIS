#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Institution Api is used
1) To view Individual Institution details.
2) To create new Institution
3) To update existing Institution
4) To list boundaries/institutions while assign permissions
"""

from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry
import simplejson
from django.template import loader, RequestContext
from klprestApi.TreeMenu import *
from schools.receivers import KLP_user_Perm


class KLP_Institution(Collection):

    """ To view selected institution details """

    def get_entry(self, institution_id):

        # Query Institution Object using Id

        institution = Institution.objects.get(id=institution_id)
        return ChoiceEntry(self, institution)


def KLP_Institution_Create(request, referKey):
    """ To Create New Institution boundary/(?P<referKey>\d+)/institution/creator/"""

    # Checking user Permissions

    KLP_user_Perm(request.user, 'Institution', 'Add')

        # Get Button Type

    buttonType = request.POST.get('form-buttonType')
    selCategoryTyp = request.POST.get('form-0-cat')
    if selCategoryTyp:
        selCategoryTyp = int(selCategoryTyp)

    # get parent boundary object for institution.

    boundaryObj = Boundary.objects.get(pk=referKey)
    institutionType = 'Institution'
    category_type = 1
    if boundaryObj.boundary_category.boundary_category.lower() \
        == 'circle':

        # if boundary category is circle then institutionType is Anganwadi and  category_type is 2 else institutionType is Institution and  category_type is 1

        institutionType = 'Anganwadi'
        category_type = 2

    # Query for Institution Category based on  category_type

    categoryList = \
        Institution_Category.objects.filter(category_type=category_type)

        # before Institution.objects.all()

    KLP_Create_Institution = \
        KLP_Institution(queryset=Institution.objects.filter(pk=0),
                        permitted_methods=('GET', 'POST'),
                        responder=TemplateResponder(template_dir='viewtemplates'
                        , template_object_name='institution',
                        extra_context={
        'buttonType': buttonType,
        'referKey': referKey,
        'institutionType': institutionType,
        'categoryList': categoryList,
        'selCategoryTyp': selCategoryTyp,
        }), receiver=XMLReceiver())
    response = KLP_Create_Institution.responder.create_form(request,
            form_class=Institution_Form)

    return HttpResponse(response)


def KLP_Institution_View(request, institution_id):
    """ To View Selected Institution institution/(?P<institution_id>\d+)/view/?$"""

    kwrg = {'is_entry': True}

        # before Institution.objects.all()

    resp = \
        KLP_Institution(queryset=Institution.objects.filter(pk=institution_id),
                        permitted_methods=('GET', 'POST'),
                        responder=TemplateResponder(template_dir='viewtemplates'
                        , template_object_name='institution'))(request,
            institution_id, **kwrg)
    return HttpResponse(resp)


def KLP_Institution_Update(request, institution_id):
    """ To update Selected Institution institution/(?P<institution_id>\d+)/update/"""

    # Checking user Permissions

    KLP_user_Perm(request.user, 'Institution', 'Update')
    buttonType = request.POST.get('form-buttonType')
    referKey = request.POST.get('form-0-boundary')
    selCategoryTyp = request.POST.get('form-0-cat')
    if selCategoryTyp:
        selCategoryTyp = int(selCategoryTyp)
    institutionObj = Institution.objects.get(id=institution_id)
    institutionType = 'Institution'
    category_type = 1
    if institutionObj.boundary.boundary_category.boundary_category \
        == 'Circle':
        institutionType = 'Anganwadi'
        category_type = 2
    categoryList = \
        Institution_Category.objects.filter(category_type=category_type)

        # before Institution.objects.all()

    KLP_Edit_Institution = \
        KLP_Institution(queryset=Institution.objects.filter(pk=institution_id),
                        permitted_methods=('GET', 'POST'),
                        responder=TemplateResponder(template_dir='edittemplates'
                        , template_object_name='institution',
                        extra_context={
        'buttonType': buttonType,
        'referKey': referKey,
        'institutionType': institutionType,
        'categoryList': categoryList,
        'selCategoryTyp': selCategoryTyp,
        }), receiver=XMLReceiver())
    response = KLP_Edit_Institution.responder.update_form(request,
            pk=institution_id, form_class=Institution_Form)

    return HttpResponse(response)


def KLP_Institution_Boundary(
    request,
    boundary_id,
    permissionType,
    assessment_id=None,
    ):
    """ To List Institutions Under Boundary to Assign Permissions to the User """

    user = request.user  # get logged in user

    # Checking user Permissions

    KLP_user_Perm(request.user, 'Users', None)
    klp_UserGroups = user.groups.all()  # Get all user groups
    klp_GroupsList = ['%s' % usergroup.name for usergroup in
                      klp_UserGroups]
    if user.is_superuser or 'AdminGroup' in klp_GroupsList:

        # if user is super user or in AdminGroup
        # Get all users.... in Data Entry Executive, Data Entry Operator groups

        users = \
            User.objects.filter(groups__name__in=['Data Entry Executive'
                                , 'Data Entry Operator'],
                                is_active=1).order_by('username')

        # get Selected boundary object....

        boundaryObj = Boundary.objects.get(id=boundary_id)
        respDict = {
            'users': users,
            'boundary': boundaryObj,
            'permissionType': permissionType,
            'url': request.path,
            }

        # get Selected Boundary Category.

        bound_cat = \
            boundaryObj.boundary_category.boundary_category.lower()
        respDict['bound_cat'] = bound_cat
        if permissionType == 'permissions':

            # If permissionType is permissions do..

            if bound_cat in ['district', 'block', 'project']:

                # if bound_cat in "district, block, project" get active(2) child boundaries

                respDict['boundary_list'] = \
                    Boundary.objects.filter(parent=boundaryObj,
                        active=2).distinct()
            else:

                # else get all active(2) child Institutions

                respDict['institution_list'] = \
                    Institution.objects.filter(boundary=boundaryObj,
                        active=2).distinct()
        else:

            # If permissionType is not permissions
            # Get All active(2) Mapped Sg's
            # studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=assessment_id, active=2).values_list('student_group', flat=True).distinct()
            # Get Institutions based Sg's

            map_institutions_list = getAssInst([assessment_id])  # StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution__id', flat=True).distinct()
            if bound_cat == 'district':

                # if bound_cat is district query block or project level  boundaries

                boundary_list = \
                    Boundary.objects.filter(institution__pk__in=map_institutions_list,
                        active=2,
                        parent__parent=boundaryObj).values_list('parent__id'
                        , flat=True).distinct()
                respDict['boundary_list'] = \
                    Boundary.objects.filter(id__in=boundary_list,
                        active=2).distinct()
            elif bound_cat in ['block', 'project']:

                # if bound_cat in block or project query circle or cluster level  boundaries

                respDict['boundary_list'] = \
                    Boundary.objects.filter(institution__pk__in=map_institutions_list,
                        active=2, parent=boundaryObj).distinct()
            else:

                # else Query Institutions

                respDict['institution_list'] = \
                    Institution.objects.filter(id__in=map_institutions_list,
                        boundary=boundaryObj, active=2).distinct()
            respDict['assessmentId'] = assessment_id

        return render_to_response('viewtemplates/institution_list.html'
                                  , respDict,
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse('Insufficient Priviliges!')


urlpatterns = patterns(
    '',
    url(r'^boundary/(?P<referKey>\d+)/institution/creator/$',
        KLP_Institution_Create),
    url(r'^institution/(?P<institution_id>\d+)/view/?$',
        KLP_Institution_View),
    url(r'^institution/(?P<institution_id>\d+)/update/?$',
        KLP_Institution_Update),
    url(r'^boundary/(?P<boundary_id>\d+)/(?P<permissionType>\w+)/?$',
        KLP_Institution_Boundary),
    url(r'^boundary/(?P<boundary_id>\d+)/(?P<permissionType>\w+)/(?P<assessment_id>\d+)/?$'
        , KLP_Institution_Boundary),
    )
