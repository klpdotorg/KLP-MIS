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
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from schools.models import *
from schools.forms import *

from django.contrib.auth.models import User

import simplejson
from django.template import loader, RequestContext

from django.core.mail import send_mail
from klpmis.settings import *
from django.views.decorators.csrf import csrf_exempt


# from django.conf import settings

def KLP_act_form(request):
    ''' To show the admin form for activate the records '''

    # get logged in user

    user = request.user
    if user.is_anonymous():
        return HttpResponseRedirect('/login/')
    else:

        respDict = {'title': 'Karnataka Learning Partnership ',
                    'user': user}
        respTemplate = \
            render_to_response('viewtemplates/AllidsActivate_html.html'
                               , respDict)

             # render admin console template

        return HttpResponse(respTemplate)


@csrf_exempt
def KLP_Activation(request):
    """ To actiave the records>"""
    import pdb
    
    # Checking user Permissions
        # KLP_user_Perm(request.user, "Institution", "Add")
        # Get Button Type

    isExecute = True

    selCategoryTyp = request.POST.get('form-staging-modelname')
    selCategoryids = request.POST.get('form-staging-allids')

    if selCategoryids == '':
        isExecute = False
        resStr = 'Please give atleast on id'
    else:

        isExecute = False
        allids1 = selCategoryids.split(',')
        model_name1 = selCategoryTyp
        respDict = {'respStr': selCategoryTyp, 'isExecute': isExecute}

        actiontype = int(request.POST.get('form-staging-action'))
        allids = []
        for k in allids1:
            allids.append(int(k))
        modelDict = {
            'boundary': Boundary,
            'institution': Institution,
            'programme': Programme,
            'assessment': Assessment,
            'question': Question,
            'studentgroup': StudentGroup,
            'student': Student,
            'staff': Staff,
            'class': StudentGroup,
            'center': StudentGroup,
            }
        if model_name1 != 'student':
            obj = obj1 = \
                modelDict[model_name1].objects.filter(id__in=allids,
                    active=int(actiontype))
            obj3 = modelDict[model_name1].objects.filter(id__in=allids)
        else:
            obj = obj1 = \
                modelDict[model_name1].objects.filter(child__id__in=allids,
                    active=int(actiontype))
            obj3 = \
                modelDict[model_name1].objects.filter(child__id__in=allids)
        actiondic = {1: 'Deactivated', 2: 'Activated'}

        flag = len(obj1) != 0

        if len(obj3) == 0 or len(obj3) != len(allids):
            idslist3 = obj3.values_list('id')
            idlist4 = []
            for k in idslist3:
                idlist4.append(k[0])
            resStr = obj1.model._meta.module_name + ' Ids ' \
                + ','.join(str(v) for v in allids if v not in idlist4) \
                + ' are not exist .Please verify the ids .'
        elif len(obj1) != 0:

            idlist1 = obj1.values_list('id')
            resStr = obj1.model._meta.module_name + ' Ids ' \
                + ','.join(str(v1[0]) for v1 in idlist1) \
                + ' are already ' + actiondic[actiontype] \
                + ' .Please verify the ids.'
        else:

            if actiontype == 1 and model_name1 != 'student' and model_name1 != 'assessment':
                childlength = hasChildObj(allids, model_name1)
            else:
                childlength = []
            if model_name1.lower() == 'student' and actiontype == 1 and model_name1 != 'assessment':
                childi = obj3.values_list('id', flat=True)
                relObjects = \
                    Student_StudentGroupRelation.objects.filter(student__id__in=childi,
                        academic=current_academic, active=2)
                relObjects.update(active=1)
                childlength = []
            if len(childlength) == 0 :
                obj2 = obj3  # modelDict[model_name1].objects.filter(id__in=allids)
                isExecute = True
                idlist2 = obj2.values_list('id')
                idstr = ','.join(str(v1[0]) for v1 in idlist2)
                obj2.update(active=actiontype)

                SendingMail(idstr, obj2.model._meta.module_name,actiondic[actiontype])
                receiver = settings.REPORTMAIL_RECEIVER
                receiver = ','.join(str(v1) for v1 in receiver)
                if not actiondic[actiontype] == "Deactivated":
                    message = \
                    'A mail will be sent to %s as soon as all the records are activated .' \
                    % receiver
                else:
                     message = \
                    'A mail will be sent to %s as soon as all the records are deactivated .' \
                    % receiver
                resStr = obj2.model._meta.module_name + ' Ids ' + idstr \
                    + ' are Successfully ' + actiondic[actiontype] \
                    + ' .' + message
            else:
                idstr = ','.join(str(v1) for v1 in childlength)
                resStr = model_name1 + ' Ids ' + idstr \
                    + ' are having child objects.So can not delete it.First Deactivate the child objects ,then try to deactivate'
    respDict = {'respStr': resStr, 'isExecute': isExecute}

    return HttpResponse(simplejson.dumps(respDict),
                        content_type='application/json; charset=utf-8')


def hasChildObj(idlists, model_name1):
    modelDict = {
        'boundary': Boundary,
        'institution': Institution,
        'programme': Programme,
        'assessment': Assessment,
        'question': Question,
        'studentgroup': StudentGroup,
        'student': Student,
        'staff': Staff,
        'class': StudentGroup,
        'center': StudentGroup,
        }

        # Checking user Permissions

    haschildlist = []
    for k in idlists:

          # Get Object based on id and model to delete

        obj = modelDict[model_name1.lower()].objects.get(pk=k)
        if model_name1.lower() == 'boundary':
            flag = obj.getChild(obj.boundary_type)
        elif model_name1.lower() in ['class', 'studentgroup']:
            if Student_StudentGroupRelation.objects.filter(student_group__id=k,
                    active=2, academic=current_academic()).count():
                flag = True
            else:
                flag = False
        else:
            flag = obj.getChild()

        if flag:
            haschildlist.append(str(k))

    return haschildlist


def SendingMail(idlist, mname,atype):
    inst_liststr = idlist
    sender = settings.REPORTMAIL_SENDER
    receiver = settings.REPORTMAIL_RECEIVER
    if atype == "Deactivated":
        subject = 'Deactivated list'
        fullmsg = 'Following %s Ids are Deactivated  :  \n %s ' % (mname,
            inst_liststr)
    else:
        subject = 'Activated list'
        fullmsg = 'Following %s Ids are Activated  :  \n %s ' % (mname,
            inst_liststr)
    send_mail(subject, fullmsg, sender, receiver)


urlpatterns = patterns('', url(r'^KLP_activaterecords/$',
                       KLP_Activation),
                       url(r'^KLP_activaterecords_form/$',
                       KLP_act_form))
