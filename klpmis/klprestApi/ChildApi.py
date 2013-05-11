#!/usr/bin/python
# -*- coding: utf-8 -*-
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
from django.contrib.contenttypes.models import ContentType
from staging.schools.models import current_academic


class KLP_Child(Collection):

    """To Create New Child boundary/(?P<bounday>\d+)/Child/creator/"""

    def get_entry(self, child_id):
        Childs = Child.objects.get(id=child_id)
        return ChoiceEntry(self, Childs)


def KLP_Child_Create(request, referKey):
    """ To Create New Child boundary/(?P<bounday>\d+)/Child/creator/"""

    buttonType = request.POST.get('form-buttonType')

        # before Child.objects.all()

    queryset = Child.objects.filter(pk=0)
    KLP_Create_Child = KLP_Child(queryset, permitted_methods=('GET',
                                 'POST'),
                                 responder=TemplateResponder(template_dir='viewtemplates'
                                 , template_object_name='child',
                                 extra_context={'buttonType': buttonType,
                                 'referKey': referKey}),
                                 receiver=XMLReceiver())
    response = KLP_Create_Child.responder.create_form(request,
            form_class=Child_Form)
    return HttpResponse(response)


def KLP_Child_View(request, child_id):
    """ To View Selected Child Child/(?P<Child_id>\d+)/view/?$"""

    kwrg = {'is_entry': True}

        # before Child.objects.all()

    resp = KLP_Child(queryset=Child.objects.filter(pk=child_id),
                     permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(template_dir='viewtemplates'
                     , template_object_name='child'))(request,
            child_id, **kwrg)
    return HttpResponse(resp)


def KLP_Child_Update(request, child_id):
    """ To update Selected Child Child/(?P<Child_id>\d+)/update/"""

    buttonType = request.POST.get('form-buttonType')
    referKey = request.POST.get('form-0-boundary')

        # before Child.objects.all()

    KLP_Edit_Child = \
        KLP_Child(queryset=Child.objects.filter(pk=child_id),
                  permitted_methods=('GET', 'POST'),
                  responder=TemplateResponder(template_dir='edittemplates'
                  , template_object_name='child',
                  extra_context={'buttonType': buttonType,
                  'referKey': referKey}), receiver=XMLReceiver())
    response = KLP_Edit_Child.responder.update_form(request,
            pk=child_id, form_class=Child_Form)
    return HttpResponse(response)


def getStudentSearch(
    request,
    boundary,
    fieldName,
    searchtext,
    ):
    '''To get the Child details by category

          name wise to get the child details list either api/child/name/<child-name> or api/xml/child/name/<child-name>
                  
         In json format api/json/child/name/<child-name>

         date of birth wise to get the child details list either api/child/dob/yyyymmdd or api/child/dob/yyyymmdd
                  
         In json format api/json/child/dob/yyyymmdd

         sex wise to get the child details list either api/child/sex/male or api/child/sex/female
                  
         In json format api/json/child/sex/male

            
         mother language wise to get the child details list either api/child/ml/1 or api/child/ml/2
                  
         In json format api/json/ml/1'''

    queryset = []
    if fieldName == 'firstname':
        child_list = \
            Child.objects.filter(first_name__startswith=searchtext,
                                 boundary__id=boundary).values_list('id'
                , flat=True)

    if fieldName == 'lastname':
        child_list = \
            Child.objects.filter(last_name__startswith=searchtext,
                                 boundary__id=boundary).values_list('id'
                , flat=True)

    if fieldName == 'dobyear':
        child_list = Child.objects.filter(dob__year=searchtext,
                boundary__id=boundary).values_list('id', flat=True)

    if fieldName == 'dob':
        child_year = searchtext[0:4] + '-' + searchtext[4:6] + '-' \
            + searchtext[6:8]
        child_list = Child.objects.filter(dob=searchtext,
                boundary__id=boundary).values_list('id', flat=True)

    if fieldName == 'gender':
        child_list = \
            Child.objects.filter(gender__startswith=searchtext,
                                 boundary__id=boundary).values_list('id'
                , flat=True)

    if fieldName == 'mt':
        child_list = \
            Child.objects.filter(mt__name__startswith=searchtext,
                                 boundary__id=boundary).values_list('id'
                , flat=True)

    if fieldName == 'mother':
        child_list = \
            Child.objects.filter(relations__relation_type='Mother',
                                 relations__name__startswith=searchtext,
                                 boundary__id=boundary).values_list('id'
                , flat=True)

    if fieldName == 'father':
        child_list = \
            Child.objects.filter(relations__relation_type='Father',
                                 relations__name__startswith=searchtext,
                                 boundary__id=boundary).values_list('id'
                , flat=True)

    studentslist = Student.objects.exclude(child__id__in=child_list,
            school__isnull=True).values_list('child__id', flat=True)
    queryset = Child.objects.filter(id__in=child_list,
                                    boundary__id=boundary).exclude(id__in=studentslist).order_by('first_name'
            )
    return queryset


def ChildrenList(request, boundary_id):
    ''' To display the Child details according to Pagination'''

    queryset = []
    reqlist = request.GET.items()
    itemlist = [str(k[0]) for k in reqlist]
    url = '/boundary/' + boundary_id + '/child/view/'
    schools = School.objects.filter(boundary__id=boundary_id, active=2)
    studentGroups = \
        StudentGroup.objects.filter(content_type__model='boundary',
                                    object_id=boundary_id, active=2)
    if 'count' in itemlist:
        count = request.GET['count']
    else:
        count = '0'
    if 'fieldName' in itemlist or 'searchtext' in itemlist:
        fieldName = request.GET['fieldName']
        searchtext = request.GET['searchtext']
        url += '?fieldName=' + fieldName + '&searchtext=' + searchtext
        queryset = getStudentSearch(request, boundary_id, fieldName,
                                    searchtext)
    else:
        studentslist = \
            Student.objects.filter(school__isnull=False).values_list('child__id'
                , flat=True)
        queryset = Child.objects.exclude(id__in=studentslist,
                boundary__id=boundary_id).order_by('first_name')
    boundary = Boundary.objects.get(pk=boundary_id)
    val = Collection(queryset, permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(paginate_by=10,
                     template_dir='viewtemplates',
                     template_object_name='child', extra_context={
        'url': url,
        'schools': schools,
        'count': count,
        'boundary': boundary,
        'studentGroups': studentGroups,
        }), entry_class=ChoiceEntry)
    return HttpResponse(val(request))


class StdGrpFilter(Resource):

    """ To get  assessment under programme filter/(?P<programme_id>\d+)/programme/"""

    def read(self, request, school_id):
        if 1:
            stdgrp_list = \
                StudentGroup.objects.filter(content_type__model='school'
                    , object_id=school_id, group_type='Class')
            respStr = ''
            for stdgrp in stdgrp_list:
                respStr += '%s$$%s %s&&' % (stdgrp.id, stdgrp.name,
                        stdgrp.section)
            return HttpResponse(respStr[0:len(respStr) - 2])
        else:
            return HttpResponse('fail')


def childsql(request, boundary_id):
    children_id = request.POST.getlist('studentchecked')
    students_id = request.POST.getlist('students')
    count = 0
    studentgroup = request.POST['studentgroup']
    if studentgroup == 'None':
        studentgroup = ''

    if children_id and studentgroup:
        studentgroup = StudentGroup.objects.get(pk=studentgroup)
        school = School.objects.get(pk=request.POST['school'])
        academic = Academic_Year.objects.get(pk=current_academic().id)
        for child_id in children_id:
            child = Child.objects.get(pk=child_id)
            studentparam = {
                'id': None,
                'child': child,
                'school': school,
                'active': 2,
                }
            stdobj = Student.objects.get_or_create(**studentparam)

            param = {
                'id': None,
                'student': stdobj[0],
                'student_group': studentgroup,
                'academic': academic,
                'active': 2,
                }
            stdgrp_rels = \
                Student_StudentGroupRelation.objects.get_or_create(**param)
            count = count + 1
    elif students_id and studentgroup:
        studentgroup = StudentGroup.objects.get(pk=studentgroup)
        academic = Academic_Year.objects.get(pk=current_academic().id)
        for student_id in students_id:
            child = Child.objects.get(pk=student_id)
            studentparam = {'id': None, 'child': child, 'active': 2}
            stdobj = Student.objects.get_or_create(**studentparam)

            param = {
                'id': None,
                'student': stdobj[0],
                'student_group': studentgroup,
                'academic': academic,
                'active': 2,
                }
            stdgrp_rels = \
                Student_StudentGroupRelation.objects.get_or_create(**param)
            count = count + 1
    return HttpResponseRedirect('/boundary/' + str(boundary_id)
                                + '/child/view/?count=' + str(count))


urlpatterns = patterns(
    '',
    url(r'^boundary/(?P<referKey>.*)/child/creator/$',
        KLP_Child_Create),
    url(r'^child/(?P<child_id>\d+)/view/?$', KLP_Child_View),
    url(r'^child/(?P<child_id>\d+)/update/?$', KLP_Child_Update),
    url(r'^boundary/(?P<boundary_id>\d+)/child/view/$', ChildrenList),
    url(r'^filter/(?P<school_id>\d+)/schgrp/$',
        StdGrpFilter(permitted_methods=('POST', 'GET'))),
    url(r'^childsql/(?P<boundary_id>\d+)/$', childsql),
    )
