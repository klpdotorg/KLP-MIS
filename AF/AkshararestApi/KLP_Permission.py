from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils import simplejson
from django.db.models import Q	

from schools.signals import check_user_perm
from schools.receivers import KLP_user_Perm

def KLP_Assign_Permissions(request):
	check_user_perm.send(sender=None, user=request.user, model='Users', operation=None)
        check_user_perm.connect(KLP_user_Perm)
	respDict = {}
	deUserList = request.POST.getlist('assignToUser')
	permissions = request.POST.getlist('userPermission')
	permissionType = request.POST.get('permissionType')
	assessmentId = request.POST.get('assessmentId')
	bound_cat = request.POST.get('bound_cat')
	inst_list = request.POST.getlist('instName')
	bound_list = request.POST.getlist('boundaryName')
	assessmentPerm = request.POST.get('assessmentPerm')
	count, asmCount = 0, 0
	if not deUserList:
		respDict['respMsg'] = 'Select Atleast One User'
		respDict['isSuccess'] = False
	elif not permissions:
		respDict['respMsg'] = 'Select Atleast One Permission'
		respDict['isSuccess'] = False
	elif bound_cat in ['district', 'block', 'project']:
		if not bound_list:
			respDict['respMsg'] = 'Select Atleast One Boundary'
			respDict['isSuccess'] = False
		else:
			if bound_cat == 'district':
				for bound in bound_list:
					inst_list = Institution.objects.filter(boundary__parent__id = bound, active=2).values_list('id', flat=True).distinct()
					count = count + len(inst_list)
					aCount = assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId, assessmentPerm)
					asmCount = asmCount + aCount
			elif bound_cat in [ 'block', 'project']:
				for bound in bound_list:
					inst_list = Institution.objects.filter(boundary__id = bound, active=2).values_list('id', flat=True).distinct() 
					count = count + len(inst_list)
					aCount = assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId, assessmentPerm)
					asmCount = asmCount + aCount
			if assessmentPerm:
				respDict['respMsg'] = 'Assigned Permissions successfully for %s Institutions  and %s Assessments Assigned successfully' %(count, asmCount)
			else:
				respDict['respMsg'] = 'Assigned Permissions successfully for %s Institutions' %(count)
			respDict['isSuccess'] = True
		
	else:
		if not inst_list:
			respDict['respMsg'] = 'Select Atleast One Institution'
			respDict['isSuccess'] = False				
		else:
			count = count + len(inst_list)
			aCount = assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId, assessmentPerm)
			asmCount = asmCount + aCount
			if assessmentPerm:
				respDict['respMsg'] = 'Assigned Permissions successfully for  %s Institutions and %s Assessments Assigned successfully' %(count, asmCount)
			else:
				respDict['respMsg'] = 'Assigned Permissions successfully for  %s Institutions' %(count)
			respDict['isSuccess'] = True
	if count == 0:
		respDict['respMsg'] = 'No Institutions Found to Assign Permissions'
		respDict['isSuccess'] = False		
	
	return HttpResponse(simplejson.dumps(respDict), content_type='application/json; charset=utf-8')	
	
def assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId=None, assessmentPerm=None):
	count = 0
	for inst_id in inst_list:
		instObj = Institution.objects.get(pk=inst_id)
		for deUser in deUserList:
			userObj = User.objects.get(id=deUser)
			if permissionType == 'permissions':
				userObj.set_perms(permissions, instObj)
				if assessmentPerm:
					sg_list = StudentGroup.objects.filter(institution__id=inst_id).values_list('id', flat=True).distinct()
					asmIds = Assessment_StudentGroup_Association.objects.filter(student_group__id__in= sg_list, active=2).values_list("assessment__id", flat=True).distinct()
					for asmId in asmIds:
						assessmentObj = Assessment.objects.get(id=asmId)
						try:
							permObj = UserAssessmentPermissions(user = userObj, instituion = instObj, assessment = assessmentObj, access=True)
							permObj.save()
						except:
							permObj = UserAssessmentPermissions.objects.get(user = userObj, instituion = instObj, assessment = assessmentObj)
							permObj.access = True
							permObj.save()
					count = len(asmIds)
			else:
				assessmentObj = Assessment.objects.get(pk=assessmentId)
				try:
					permObj = UserAssessmentPermissions.objects.get(user = userObj, instituion = instObj, assessment = assessmentObj)
					permObj.access = True
					permObj.save()
				except :
					permObj = UserAssessmentPermissions(user = userObj, instituion = instObj, assessment = assessmentObj, access=True)
					permObj.save()
	return count	

def KLP_Users_list(request):
	user = request.user
	if user.id:
		check_user_perm.send(sender=None, user=user, model='Users', operation=None)
		check_user_perm.connect(KLP_user_Perm)
		user_list = User.objects.filter(is_active=1, is_staff=0, is_superuser=0).order_by("username")
		return render_to_response('viewtemplates/show_users_form.html',{'user_list':user_list, 'user':user, 'title':'KLP Users', 'legend':'Karnataka Learning Partnership', 'entry':"Add"})     
	else:
		return HttpResponseRedirect('/login/')
		
def KLP_User_Delete(request, user_id):
	user = request.user
	if user.id:
		check_user_perm.send(sender=None, user=user, model='Users', operation=None)
		check_user_perm.connect(KLP_user_Perm)
		import random
		import string
		rangeNum = 8
		randomStr = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(rangeNum))
		userObj = User.objects.get(pk=user_id)
		userObj.is_active = 0
		userObj.set_password(randomStr)
		userObj.save()
		return render_to_response('viewtemplates/userAction_done.html',{'user':request.user,'selUser':userObj,'message':'User Deletion Successful', 'legend':'Karnataka Learning Partnership', 'entry':"Add"})       
	else:
		return HttpResponseRedirect('/login/')
	
def KLP_User_Permissions(request, user_id):
	user = request.user
	if user.id:
		check_user_perm.send(sender=None, user=user, model='Users', operation=None)
		check_user_perm.connect(KLP_user_Perm)
		userObj = User.objects.get(pk=user_id)
		boundType_List = Boundary_Type.objects.all()
		try:
			sessionVal = int(request.session['session_sch_typ'])
		except:
			sessionVal = 0
	
		return render_to_response('viewtemplates/user_permissions.html',{'userId':user_id, 'userName':userObj.username, 'boundType_List':boundType_List, 'home':True, 'session_sch_typ':sessionVal, 'entry':"Add",  'shPerm':True, 'title':'KLP Permissions', 'legend':'Karnataka Learning Partnership'}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')
	
	
def KLP_Show_Permissions(request, boundary_id, user_id):
	userObj = User.objects.get(pk=user_id)
	boundType_List = Boundary_Type.objects.all()
	try:
		sessionVal = int(request.session['session_sch_typ'])
	except:
		sessionVal = 0
	redUrl = '/list/%s/user/%s/permissions/' %(boundary_id, user_id)
	assignedInst = Institution.objects.select_related("boundary").filter(Q(boundary__id=boundary_id)|Q(boundary__parent__id=boundary_id)|Q(boundary__parent__parent__id=boundary_id), active=2).extra(where=['''schools_institution.id in (SELECT "obj_id" FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = 't')''' %(user_id)]).only("id", "name", "boundary").order_by("boundary", "boundary__parent", "name")
	
	assignedInstIds = assignedInst.values_list("id", flat=True)
	unAssignedInst = Institution.objects.select_related("boundary").filter(Q(boundary__id=boundary_id)|Q(boundary__parent__id=boundary_id)|Q(boundary__parent__parent__id=boundary_id), active=2).exclude(pk__in=assignedInstIds).only("id", "name", "boundary").order_by("boundary", "boundary__parent", "name")
	
	
	
	assignedpermObjects = UserAssessmentPermissions.objects.select_related("assessment", "instituion").filter(Q(instituion__boundary__id=boundary_id)|Q(instituion__boundary__parent__id=boundary_id)|Q(instituion__boundary__parent__parent__id=boundary_id), user=userObj, access=True).defer("access").order_by("instituion__boundary", "instituion__boundary__parent", "instituion__name",)
	
	
	
	unMapObjs = Assessment_StudentGroup_Association.objects.select_related("student_group", "assessment").filter(Q(student_group__institution__boundary__id=boundary_id)|Q(student_group__institution__boundary__parent__id=boundary_id)|Q(student_group__institution__boundary__parent__parent__id=boundary_id), active=2).defer("active").order_by("student_group__institution__boundary", "student_group__institution__boundary__parent", "student_group__institution__name")
	for assignedPermObj in assignedpermObjects:
		qsets = (
	            Q(assessment = assignedPermObj.assessment)&
	            Q(student_group__institution = assignedPermObj.instituion)
	        )
		unMapObjs = unMapObjs.exclude(qsets)
	unMapList = unMapObjs.values_list("student_group__institution", "assessment").distinct()
	
	qList=[Assessment_StudentGroup_Association.objects.select_related("student_group", "assessment").filter(student_group__institution__id=unMapVal[0], assessment__id=unMapVal[1]).defer("active")[0] for unMapVal in unMapList]
	
	return render_to_response('viewtemplates/show_permissions.html',{'assignedInst':assignedInst,  'userId':user_id, 'userName':userObj.username, 'unAssignedInst':unAssignedInst, 'assignedpermObjects':assignedpermObjects, 'redUrl':redUrl, 'qList':qList}, context_instance=RequestContext(request))		
	
def KLP_Show_User_Permissions(request, boundary_id, user_id):	
	return render_to_response('viewtemplates/show_permissions.html',{'userId':user_id, 'boundary_id':boundary_id, 'confirmMsg':True}, context_instance=RequestContext(request))	 
	
	
def KLP_Revoke_Permissions(request, permissionType):
	check_user_perm.send(sender=None, user=request.user, model='Users', operation=None)
	check_user_perm.connect(KLP_user_Perm)
	user_id = request.POST.get('userId')
	opStatus = "success"
	try:
		if permissionType == 'permissions':
			userObj = User.objects.get(pk=user_id)
			instList = request.POST.getlist('assignedInst')
			for inst_id in instList:
				instObj = Institution.objects.get(pk=inst_id)
				userObj.revoke('Acess', instObj)
		else:
			assignedAsmList = request.POST.getlist('assignedAsm')
			for userAsm_id in assignedAsmList:
				permObj = UserAssessmentPermissions.objects.get(pk=userAsm_id)
				permObj.access = False
				permObj.save()
	except:
		opStatus = "fail"		
	return HttpResponse(opStatus)
	
def KLP_ReAssign_Permissions(request, permissionType):
	check_user_perm.send(sender=None, user=request.user, model='Users', operation=None)
	check_user_perm.connect(KLP_user_Perm)
	userList = request.POST.getlist('userId')
	permissions = ['Acess']
	opStatus = "success"
	try:
		if permissionType== 'permissions':
			inst_list = request.POST.getlist('unassignedInst')
			assignPermission(inst_list, userList, permissions, permissionType, None, True)
		else:
			asmList = request.POST.getlist('unassignedAsm')
			for asm in asmList:
				asm_list = asm.split("_")
				inst_list = [asm_list[0]]
				assessmentId = asm_list[1]
				assignPermission(inst_list, userList, permissions, permissionType, assessmentId)
	except:
		opStatus = "fail"		
	return HttpResponse(opStatus)

urlpatterns = patterns('',             
   url(r'^assign/permissions/?$', KLP_Assign_Permissions),
   url(r'^list/users/?$', KLP_Users_list),
   url(r'^user/(?P<user_id>\d+)/delete?$', KLP_User_Delete),
   url(r'^user/(?P<user_id>\d+)/permissions/?$', KLP_User_Permissions),
   url(r'^list/(?P<boundary_id>\d+)/user/(?P<user_id>\d+)/permissions/?$', KLP_Show_Permissions),
   url(r'^revoke/user/(?P<permissionType>\w+)/?$', KLP_Revoke_Permissions),
   url(r'^assign/user/(?P<permissionType>\w+)/?$', KLP_ReAssign_Permissions),
   url(r'^show/(?P<boundary_id>\d+)/user/(?P<user_id>\d+)/permissions/?$', KLP_Show_User_Permissions),
)
