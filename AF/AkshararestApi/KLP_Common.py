"""
KLP_common is used
1) To create new node for tree on creation of new boundary, institution, sg, programme, assessment and question.
2) To Delete (deactive object) boundary, institution, sg, staff, programme, assessment and question.
"""
from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *

from schools.receivers import KLP_user_Perm

class KLP_Create_Node(Resource):    
    def read(self, request, model_name, new_id):
    	""" This method uses to create new node for tree on creation of  boundary,  institution, programme, assessment, question and  studentgroup"""
	objDict = {'boundary':Boundary, 'institution':Institution, 'programme':Programme, 'assessment':Assessment, 'question':Question, 'studentgroup':StudentGroup,}
	boundaryType =  request.GET.get('boundaryType')
	modelObj = objDict[model_name]
	# Get Object based on id and model
        GetData = modelObj.objects.get(pk=new_id)
        # Call CreateNewFolder Method
	if model_name == 'boundary':
		return HttpResponse(GetData.CreateNewFolder(boundaryType))
        return HttpResponse(GetData.CreateNewFolder())

class KLP_Delete(Resource):    
    """ To delete boundary,  institution, programme, assessment, question and  studentgroup delete/(?P<model_name>\w+)/(?P<referKey>\d+)/"""
    def read(self,request,model_name, referKey):
        modelDict = {'boundary':Boundary, 'institution':Institution, 'programme':Programme, 'assessment':Assessment, 'question':Question, 'studentgroup':StudentGroup, 'student':Student, 'staff':Staff, 'class':StudentGroup, 'center':StudentGroup}
        # Checking user Permissions
        KLP_user_Perm(request.user, modelDict[model_name.lower()]._meta.module_name, "Delete")
        # Get Object based on id and model to delete
        obj = modelDict[model_name.lower()].objects.get(pk=referKey)
	if model_name == 'student':
		Student_StudentGroupRelation.objects.filter(student__id = referKey).update(active=0)
        obj.active=0 # Change active to 0(object is deleted)
        obj.save() # Save Data
        return HttpResponse('Deleted')
        

urlpatterns = patterns('',
   url(r'^delete/(?P<model_name>\w+)/(?P<referKey>\d+)/$', KLP_Delete(permitted_methods=('POST','GET'))),
   url(r'^createnew/(?P<model_name>\w+)/(?P<new_id>\d+)/$', KLP_Create_Node(permitted_methods=('POST','GET'))),
   
)        
