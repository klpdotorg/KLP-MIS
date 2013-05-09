"""
KLP_Permission file is used
1) To assign permissions
2) To list users
3) To Delete users
4) To show permissions at diffrent level of boundaries
5) To revoke user permissions
6) To reassign permissions to user.
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
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils import simplejson
from django.db.models import Q
from django.core.management import call_command
from schools.receivers import KLP_user_Perm
from django.conf import settings
from subprocess import Popen
from subprocess import call
from klprestApi.TreeMenu import KLP_assignedInstitutions


def KLP_Assign_Permissions(request):
    """ This method is used to assign permissions"""
    """ Check logged in user permissions to assign permissions"""
    KLP_user_Perm(request.user, "Users", None)
    respDict = {}
    # get selected users list to assign permissions
    deUserList = request.POST.getlist('assignToUser')
    #get selected permissions list
    permissions = request.POST.getlist('userPermission')
    # get permission type
    receiver = settings.REPORTMAIL_RECEIVER
    receiver = ','.join(str(v1) for v1 in receiver)
    message = "A mail will be sent to %s as soon as\
    all the permissions are assigned" % (receiver)
    permissionType = request.POST.get('permissionType')
    # get assessment Id to assign assessment permissions
    assessmentId = request.POST.get('assessmentId')
    # get boundary category
    bound_cat = request.POST.get('bound_cat')
    # get selected institutions list
    inst_list = request.POST.getlist('instName')
    # get selected boundaries list
    bound_list = request.POST.getlist('boundaryName')
    # get assessment permission (True or False)
    assessmentPerm = request.POST.get('assessmentPerm')
    print deUserList, permissions, message, permissionType,
    assessmentId, bound_cat,
    inst_list, bound_list,
    assessmentPermcount, asmCount, assignedAsmIds = 0, 0, []
    bound_list = ','.join(str(v1) for v1 in bound_list if v1 > 0)
    permissions = ','.join(str(v1) for v1 in permissions if v1 > 0)
    deUserList = ','.join(str(v1) for v1 in deUserList if v1 > 0)
    if not deUserList:
        # If no users selected respond back with error message
        #(Select Atleast One User)
        respDict['respMsg'] = 'Select Atleast One User'
        respDict['isSuccess'] = False
    elif not permissions:
        # if permissions not selected respond back with error
        #message (Select Atleast One Permission)
        respDict['respMsg'] = 'Select Atleast One Permission'
        respDict['isSuccess'] = False
    elif bound_cat in ['district', 'block', 'project']:
        # if bound category in 'district', 'block', 'project'
        #check for boundary list
        if not bound_list:
            # if boundary list is empty respond back with error
            #message (Select Atleast One Boundary)
            respDict['respMsg'] = 'Select Atleast One Boundary'
            respDict['isSuccess'] = False
        else:
            #bound_list=','.join(str(v1) for v1 in bound_list if v1 > 0)
            Popen(["python", "/home/klp/production/manage.py",
            "KLP_assignPermissions", str(inst_list), str(deUserList),
            str(permissions), str(permissionType),
            str(assessmentId), str(assessmentPerm),
            bound_cat, bound_list, request.user.username])
            #call(["/home/c2staging/c2staging/bin/python" ,
            #"/home/c2staging/c2staging/c2staging/manage.py",
            #"KLP_assignPermissions",str(inst_list),
            #str(deUserList),str(permissions),str(permissionType),
            #str(assessmentId),str(assessmentPerm),
            #bound_cat,bound_list])
            #'Assigned Permissions successfully for %s Institutions' %(count)
            respDict['respMsg'] = message
            respDict['isSuccess'] = True
            #Tosendmailteam(inst_list,deUserList,permissions,
            #permissionType,assessmentId,assessmentPerm)
    else:
        # if bound category in 'cluste' or 'circle' check for institution list
        if not inst_list:
            # if institutions list is empty  respond back with
            #error message (Select Atleast One Institution)
            respDict['respMsg'] = 'Select Atleast One Institution'
            respDict['isSuccess'] = False
        else:
            # get count of institutions to show count of assigned
            #institution objects to user
            count = count + len(inst_list)
            # call assignPermission method to assign permissions
            inst_list = ','.join(str(v1) for v1 in inst_list if v1 > 0)
            print "FDFDF", bound_cat, bound_list, "HREEEEEEE"
            Popen(["python", "/home/klp/production/manage.py",
            "KLP_assignPermissions", str(inst_list), str(deUserList),
            str(permissions), str(permissionType), str(assessmentId),
            str(assessmentPerm), bound_cat, str(bound_list).strip(),
            request.user.username])
            respDict['respMsg'] = message  # Assigned Permissions
            #successfully for  %s Institutions' %(count)
            respDict['isSuccess'] = True
            #Tosendmailteam(inst_list,deUserList,permissions,
            #permissionType,assessmentId,assessmentPerm)
    return HttpResponse(simplejson.dumps(respDict),
    content_type='application/json; charset=utf-8')


def assignPermission(inst_list, deUserList, permissions, permissionType,
assessmentId=None, assessmentPerm=None):
    assignedAsmIds = []
    print inst_list, "SSSSSSSSSSs"
    assignedInsIds = []
    if assessmentId:
        assessmentObjsel = Assessment.objects.get(id=assessmentId)
    for inst_id in inst_list:
        # get Institution object using id
        inst_id = int(inst_id)
        instObj = Institution.objects.get(pk=inst_id)
        for deUser in deUserList:
            # get user object
            deUser = int(deUser)
            userObj = User.objects.get(id=deUser)
            if assessmentPerm!=None and assessmentPerm!='None':
                uobj = UserAssessmentPermissions.objects.filter(
                user=userObj, instituion= instObj,
                assessment=assessmentObjsel)
                if uobj:
                    uflag = True
                else:
                    uflag = False
            else:
                uflag = True
                if uflag:
                    print userObj, permissionType
                    assignedInsIds.append(inst_id)
            if permissionType == 'permissions':
                # if permission type is permissions set institution
                #level permissions for the user
                userObj.set_perms(permissions, instObj)
                if assessmentPerm != None and assessmentPerm != 'None':
                    # if assessmentPerm is true assign assessment
                    #also to the user.
                    sg_list = StudentGroup.objects.filter(
                    institution__id=inst_id).values_list('id',
                    flat=True).distinct()
                    print sg_list[:10], inst_id
                    #print sg_list
                    asess = Assessment_StudentGroup_Association.objects.filter
                    asmIds = asess(
                    student_group__id__in=sg_list,
                    active=2).values_list("assessment__id",
                    flat=True).distinct()
                    print asmIds
                    for asmId in asmIds:
                        assessmentObj = Assessment.objects.get(id=asmId)
                        try:
                            permObj = UserAssessmentPermissions.objects.get(
                            user = userObj,
                            instituion = instObj,
                            assessment = assessmentObj)
                            permObj.access = True
                            permObj.save()
                        except:
                            print "EXT"
                            permObj = UserAssessmentPermissions(user = userObj,
                            instituion = instObj, assessment =
                            assessmentObj, access=True)
                            try:
                                permObj.save()
                            except:
                                pass
                                assignedAsmIds.extend(asmIds)
            else:
                # else assign assessment permissions to user.
                assessmentObj = Assessment.objects.get(pk=assessmentId)
                try:
                    permObj = UserAssessmentPermissions.objects.get(
                    user = userObj, instituion = instObj,
                    assessment = assessmentObj)
                    permObj.access = True
                    permObj.save()
                except:
                    permObj = UserAssessmentPermissions(user = userObj,
                    instituion = instObj, assessment =
                    assessmentObj, access=True)
                    permObj.save()
                    assignedAsmIds = list(set(assignedAsmIds))
                    print assignedAsmIds, "total"
    return assignedInsIds


def KLP_Users_list(request):
    """ This method is used to list out active(1) users other
    than staff and super users"""
    # get logged in user
    user = request.user
    if user.id:
        # check logged in user permissions, to get user list
        KLP_user_Perm(request.user, "Users", None)
        # get all active(1) users list other than staff and
        #super user order by username
        user_list = User.objects.filter(is_staff=0, is_superuser=0).order_by(
        "username")
        # render show users form with users list
        return render_to_response(
        'viewtemplates/show_users_form.html',
        {'user_list': user_list, 'user': user, 'title': 'KLP Users',
        'legend': 'Karnataka Learning Partnership',
        'entry': "Add"}, context_instance=RequestContext(request))
    else:
        # if user is not logged in redirect to login page
        return HttpResponseRedirect('/login/')


def KLP_User_Activate(request, user_id):
        """ This method is used to (activate) user"""
        # get logged in user
        user = request.user
        if user.id:
            # check logged in user permissions to delete user
            KLP_user_Perm(request.user, "Users", None)
            userObj = User.objects.get(pk=user_id)
            userObj.is_active = 1  # activate user
            userObj.save()  # save user object
            return render_to_response(
            'viewtemplates/userAction_done.html',
            {'user': request.user, 'selUser': userObj,
            'message': 'User Activated Successfully',
            'legend': 'Karnataka Learning Partnership',
            'entry': "Add"}, context_instance=RequestContext(request))
        else:
            # if user is not logged in redirect to login page
            return HttpResponseRedirect('/login/')


def KLP_User_Delete(request, user_id):
    """ This method is used to delete(deactivate) user"""
    # get logged in user
    user = request.user
    if user.id:
        # check logged in user permissions to delete user
        KLP_user_Perm(request.user, "Users", None)
        import random
        import string
        rangeNum = 8
        # generate random string to replace existing password.
        randomStr = ''.join(random.choice(string.ascii_uppercase
        + string.digits) for x in range(rangeNum))
        # get user object
        userObj = User.objects.get(pk=user_id)
        userObj.is_active = 0  # deactivate user
        #userObj.set_password(randomStr)
        # replace password with random string
        userObj.save()  # save user object
        return render_to_response(
        'viewtemplates/userAction_done.html',
        {'user': request.user, 'selUser': userObj,
        'message': 'User Deletion Successful',
        'legend': 'Karnataka Learning Partnership',
        'entry': "Add"},
        context_instance=RequestContext(request))
    else:
        # if user is not logged in redirect to login page
        return HttpResponseRedirect('/login/')


def KLP_User_Permissions(request, user_id):
    """ This method is used to show tree for the selected
    user to show permissions"""
    # get logged in user
    user = request.user
    if user.id:
        # check logged in user permissions
        KLP_user_Perm(request.user, "Users", None)
        # get user object
        userObj = User.objects.get(pk=user_id)
        # get all boundary types
        boundType_List = Boundary_Type.objects.all()
        try:
            sessionVal = int(request.session['session_sch_typ'])
        except:
            sessionVal = 0
        # render user permissions template
        return render_to_response('viewtemplates/user_permissions.html',
        {'userId': user_id, 'userName': userObj.username,
        'boundType_List': boundType_List, 'home': True,
        'session_sch_typ': sessionVal, 'entry': "Add",
        'shPerm': True, 'title': 'KLP Permissions',
        'legend': 'Karnataka Learning Partnership'},
        context_instance=RequestContext(request))
    else:
        # if user is not logged in redirect to login page
        return HttpResponseRedirect('/login/')


def KLP_Show_Permissions(request, boundary_id, user_id):
    """ This method is used to show user permissions """
    userObj = User.objects.get(pk=user_id)  # get user object
    boundType_List = Boundary_Type.objects.all()  # get all boundary types
    # get session value, if session is not set default value is 0
    try:
        sessionVal = int(request.session['session_sch_typ'])
    except:
        sessionVal = 0
    redUrl = '/list/%s/user/%s/permissions/' % (boundary_id, user_id)
    # get all assigned institutions to the user
    assignedInst = Institution.objects.select_
    related("boundary").filter(
    Q(boundary__id=boundary_id) | Q(
    boundary__parent__id = boundary_id) | Q(
    boundary__parent__parent__id = boundary_id),
    active=2).extra(where
    =['''schools_institution.id in (SELECT
    "obj_id" FROM "public"."object_permissions_institution_perms"
    WHERE "user_id" = '%s' AND "Acess" = 't')''' % (
    user_id)]).only("id", "name", "boundary").order_by(
    "boundary", "boundary__parent", "name")

    assignedInstIds = assignedInst.values_list("id", flat=True)
    # get unassigned institutions based on assigned institutions
    unAssignedInst = Institution.objects.select_related("boundary").filter(
    Q(boundary__id=boundary_id) |
    Q(boundary__parent__id=boundary_id) |
    Q(boundary__parent__parent__id=boundary_id),
    active=2).exclude(pk__in=assignedInstIds).only(
    "id", "name", "boundary").order_by(
    "boundary", "boundary__parent", "name")
    # get all assigned assessment objects
    assignedpermObjects = UserAssessmentPermissions.objects.select_related(
    "assessment", "instituion").filter(
    Q(instituion__boundary__id=boundary_id) | Q(
    instituion__boundary__parent__id
    =boundary_id) | Q(instituion__boundary__parent__parent__id=boundary_id),
    user=userObj,
    access=True).defer("access").order_by(
    "instituion__boundary",
    "instituion__boundary__parent", "instituion__name",)
    unMapObjs = Assessment_StudentGroup_Association.objects.select_related(
    "student_group",
    "assessment").filter(Q(
    student_group__institution__boundary__id=boundary_id) | Q(
    student_group__institution__boundary__parent__id
    =boundary_id) | Q(
    student_group__institution__boundary__parent__parent__id=boundary_id),
    active=2).defer("active").order_by(
    "student_group__institution__boundary",
    "student_group__institution__boundary__parent",
    "student_group__institution__name")
    for assignedPermObj in assignedpermObjects:
        qsets = (Q(assessment = assignedPermObj.assessment) & Q(
        student_group__institution = assignedPermObj.instituion))
        unMapObjs = unMapObjs.exclude(qsets)
        unMapList = unMapObjs.values_list("student_group__institution",
        "assessment").distinct()
        # get all unassigned assessment objects
        qList = [Assessment_StudentGroup_Association.objects.select_related(
        "student_group", "assessment").filter(
        student_group__institution__id=unMapVal[0],
        assessment__id = unMapVal[1]).defer("active")[0]
        for unMapVal in unMapList]
    return render_to_response(
    'viewtemplates/show_permissions.html',
    {'assignedInst': assignedInst, 'userId': user_id,
    'userName': userObj.username,
    'unAssignedInst': unAssignedInst,
    'assignedpermObjects': assignedpermObjects,
    'redUrl': redUrl, 'qList': qList},
    context_instance=RequestContext(request))


def KLP_Show_User_Permissions(request, boundary_id, user_id):
    return render_to_response(
    'viewtemplates/show_permissions.html',
    {'userId': user_id, 'boundary_id': boundary_id,
    'confirmMsg': True},
    context_instance=RequestContext(request))


def KLP_Revoke_Permissions(request, permissionType):
    """ This method is used to revoke user permissions"""
    # check logged in user permissions
    KLP_user_Perm(request.user, "Users", None)
    # get user id to revoke permissions
    user_id = request.POST.get('userId')
    opStatus = "success"
    try:
        if permissionType == 'permissions':
            # if permissiontype is permissions revoke institution
            #permissions for the user
            userObj = User.objects.get(pk=user_id)
            # get institution list to revoke
            instList = request.POST.getlist('assignedInst')
            for inst_id in instList:
                instObj = Institution.objects.get(pk=inst_id)
                # revoke permission for user
                userObj.revoke('Acess', instObj)
        else:
            # else revoke assessment permissions
            assignedAsmList = request.POST.getlist('assignedAsm')
            for userAsm_id in assignedAsmList:
                # get UserAssessmentPermissions object
                permObj = UserAssessmentPermissions.objects.get(pk=userAsm_id)
                permObj.access = False  # revoke permissions
                permObj.save()
    except:
        opStatus = "fail"
    # if revoke permission fail return response as fail else return success.
    return HttpResponse(opStatus)


def KLP_ReAssign_Permissions(request, permissionType):
    """ This method is used to reassign permissions to user"""
    # check logged in user permissions
    KLP_user_Perm(request.user, "Users", None)
    #get selected users list
    userList = request.POST.getlist('userId')
    permissions = ['Acess']
    opStatus = "success"
    try:
        if permissionType == 'permissions':
            # if permissionsType is permissions assign instituions to user
            # get selected institution list
            inst_list = request.POST.getlist('unassignedInst')
            # call assignPermission method to assign permission
            assignPermission(inst_list, userList, permissions,
            permissionType, None, True)
        else:
            # else assign assessments to user
            # get selected assesment and institution list
            asmList = request.POST.getlist('unassignedAsm')
            for asm in asmList:
                asm_list = asm.split("_")
                inst_list = [asm_list[0]]
                assessmentId = asm_list[1]
                # call assignPermission method to assign permission
                assignPermission(inst_list, userList,
                permissions, permissionType, assessmentId)
    except:
        opStatus = "fail"
    # if reassign permission fail return response as fail else return success.
    return HttpResponse(opStatus)


urlpatterns = patterns('',
    url(r'^assign/permissions/?$', KLP_Assign_Permissions),
    url(r'^list/users/?$', KLP_Users_list),
    url(r'^user/(?P<user_id>\d+)/delete?$', KLP_User_Delete),
    url(r'^user/(?P<user_id>\d+)/activateuser?$', KLP_User_Activate),
    url(r'^user/(?P<user_id>\d+)/permissions/?$', KLP_User_Permissions),
    url(r'^list/(?P<boundary_id>\d+)/user/(?P<user_id>\d+)\
    /permissions/?$', KLP_Show_Permissions),
    url(r'^revoke/user/(?P<permissionType>\w+)/?$', KLP_Revoke_Permissions),
    url(r'^assign/user/(?P<permissionType>\w+)/?$', KLP_ReAssign_Permissions),
    url(r'^show/(?P<boundary_id>\d+)/user/(?P<user_id>\d+)\
    /permissions/?$', KLP_Show_User_Permissions),)
