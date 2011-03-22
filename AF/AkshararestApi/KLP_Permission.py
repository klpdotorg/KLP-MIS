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
	count = 0
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
					assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId)
			elif bound_cat in [ 'block', 'project']:
				for bound in bound_list:
					inst_list = Institution.objects.filter(boundary__id = bound, active=2).values_list('id', flat=True).distinct() 
					count = count + len(inst_list)
					assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId)
			respDict['respMsg'] = 'Assigned Permissions successfully for %s Institutions' %(count)
			respDict['isSuccess'] = True
		
	else:
		if not inst_list:
			respDict['respMsg'] = 'Select Atleast One Institution'
			respDict['isSuccess'] = False				
		else:
			status = assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId)
			respDict['respMsg'] = 'Assigned Permissions successfully for  %s Institutions' %(count)
			respDict['isSuccess'] = True
	if count == 0:
		respDict['respMsg'] = 'No Institutions Found to Assign Permissions'
		respDict['isSuccess'] = False		
	
	return HttpResponse(simplejson.dumps(respDict), content_type='application/json; charset=utf-8')	
	
def assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId=None):
	for inst_id in inst_list:
		instObj = Institution.objects.get(pk=inst_id)
		for deUser in deUserList:
			userObj = User.objects.get(id=deUser)
			if permissionType == 'permissions':
				userObj.set_perms(permissions, instObj)
			else:
				assessmentObj = Assessment.objects.get(pk=assessmentId)
				try:
					permObj = UserAssessmentPermissions(user = userObj, instituion = instObj, assessment = assessmentObj, access=True)
					permObj.save()
				except:
					permObj = UserAssessmentPermissions.objects.get(user = userObj, instituion = instObj, assessment = assessmentObj)
					permObj.access = True
					permObj.save()
	return 'success'	

def KLP_Users_list(request):
	user = request.user
	check_user_perm.send(sender=None, user=request.user, model='Users', operation=None)
        check_user_perm.connect(KLP_user_Perm)
	user_list = User.objects.filter(is_active=1, is_staff=0, is_superuser=0)
	return render_to_response('viewtemplates/show_users_form.html',{'user_list':user_list, 'user':user})     
		
def KLP_User_Delete(request, user_id):
	check_user_perm.send(sender=None, user=request.user, model='Users', operation=None)
        check_user_perm.connect(KLP_user_Perm)
	import random
	import string
	rangeNum = 8
        randomStr = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(rangeNum))
	userObj = User.objects.get(pk=user_id)
	userObj.is_active = 0
	userObj.set_password(randomStr)
	userObj.save()
	return render_to_response('viewtemplates/userAction_done.html',{'user':request.user,'selUser':userObj,'message':'User Deletion Successful'})        
	
def KLP_Show_Permissions(request, user_id):
	check_user_perm.send(sender=None, user=request.user, model='Users', operation=None)
	check_user_perm.connect(KLP_user_Perm)
	userObj = User.objects.get(pk=user_id)
	rawQuerySet = Institution.objects.raw(""" SELECT * FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = 't' """ %(user_id))
	inst_list=[]
	for permObj in rawQuerySet:
		instObj = Institution.objects.get(pk=permObj.obj_id)
		ins_dict = {'Institute':instObj.name, 'instId':instObj.id, 'Acess':permObj.Acess}
		inst_list.append(ins_dict)
	permObjects = UserAssessmentPermissions.objects.filter(user=userObj, access=True)	
	return render_to_response('viewtemplates/show_permissions.html',{'inst_list':inst_list, 'userName':userObj.username, 'userId':user_id, 'entry':"Add", 'permObjects':permObjects})
	
def KLP_Flush_Permissions(request, permissionType):
	check_user_perm.send(sender=None, user=request.user, model='Users', operation=None)
	check_user_perm.connect(KLP_user_Perm)
	user_id = request.POST.get('userId')
	inst_id = request.POST.get('inst_id')
	userObj = User.objects.get(pk=user_id)
	instObj = Institution.objects.get(pk=inst_id)
	if permissionType == 'permissions':
		userObj.revoke('Acess', instObj)
	else:
		permObj = UserAssessmentPermissions.objects.get(user = userObj, instituion = instObj, assessment__id = request.POST.get('assessmentId'))
		permObj.access = False
		permObj.save()
	return HttpResponse("success")


urlpatterns = patterns('',             
   url(r'^assign/permissions/?$', KLP_Assign_Permissions),
   url(r'^list/users/?$', KLP_Users_list),
   url(r'^user/(?P<user_id>\d+)/delete?$', KLP_User_Delete),
   url(r'^user/(?P<user_id>\d+)/show/permissions/?$', KLP_Show_Permissions),
   url(r'^flush/user/(?P<permissionType>\w+)/?$', KLP_Flush_Permissions),
)
