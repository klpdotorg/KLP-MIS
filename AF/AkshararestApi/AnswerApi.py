from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
from django.template import Template, Context, RequestContext
from schools.forms import *
from schools.models import *
from django_restapi.authentication import *

from schools.signals import check_perm
from schools.receivers import KLP_obj_Perm
         
def KLP_DataEnry(request):
        return HttpResponse(KLP_ChangeAns(permitted_methods=('POST','PUT','GET','DELETE')).read(request))
class KLP_ChangeAns(Resource):
    """ To Create and Edit Answers answer/data/entry/"""
    def read(self,request):
    	user = request.user
        student =  request.POST.get('student')
        programId = request.POST.get('programId')
        assessmentId = request.POST.get('assessmentId')
        student_groupId = request.POST.get('student_groupId')
        studentObj = Student.objects.filter(pk=student).defer("child")[0]
        Questions_list = Question.objects.filter(assessment__id=assessmentId).defer("assessment")
        student_groupObj = StudentGroup.objects.filter(pk = student_groupId).values("institution")[0]
        assessmentObj = Assessment.objects.filter(pk=assessmentId).defer("programme")[0]
        instObj = Institution.objects.filter(pk=student_groupObj["institution"]).defer("boundary")[0]
        check_perm.send(sender=None, user=user, instance=instObj, Assessment=assessmentObj, permission='Acess')
        check_perm.connect(KLP_obj_Perm)
        for question in Questions_list:
        	textField = 'student_%s_%s' %(student, question.id)
        	textFieldVal = request.POST.get(textField)
        	try:
        		ansObj = Answer.objects.filter(question = question, student = studentObj).defer("question", "student")[0]
        		if textFieldVal:
        			if textFieldVal.lower() == 'ab':
        				ansObj.answerGrade = None
        				ansObj.answerScore = None
        				ansObj.status = -99999
        			elif textFieldVal.lower() == 'uk':
        				ansObj.answerGrade = None
        				ansObj.answerScore = None
        				ansObj.status = -1
        			elif question.questionType == 2:
        				ansObj.status = None
        				ansObj.answerGrade = textFieldVal
        			else:
        				ansObj.status = None	
        				ansObj.answerScore = textFieldVal
        			if ansObj.doubleEntry == 1 and ansObj.user1 == user:
					ansObj.lastmodifiedBy = user
				else:
					ansObj.doubleEntry = 2
					ansObj.lastmodifiedBy = user
				       	ansObj.user2 = user
        			ansObj.save()	
        	except :
        		if textFieldVal:
				ansObj = Answer(question=question, student=studentObj, doubleEntry=1)
				ansObj.save()
				if textFieldVal.lower() == 'ab':
					ansObj.status = -99999
				elif textFieldVal.lower() == 'uk':
					ansObj.status = -1
				elif question.questionType == 2:
        				ansObj.answerGrade = textFieldVal
        			else:
        				ansObj.answerScore = textFieldVal
        			ansObj.lastmodifiedBy = user	
        			ansObj.user1 = user
        			ansObj.save()
	        
	return "Data Saved"


def KLP_DataValidation(request):
    """ To Validate data for Doble Entry answer/data/validation/"""
    validateId = request.POST.get('validateField')
    validateValue = request.POST.get('validateValue')
    listIds = validateId.split('_')
    ansObj = Answer.objects.filter(student__id=listIds[1], question__id=listIds[2]).defer("student","user1", "user2", "lastmodifiedBy")[0]
    respStr = False
    dEntry = int(ansObj.doubleEntry)
    if dEntry in [0,2]:
    	respStr = True
    else:
    	if validateValue:
	    	if validateValue.lower() == 'ab':
	    		if ansObj.status == -99999:
	    			respStr = True
	    	elif validateValue.lower() == 'uk':
	    		if ansObj.status == 0:
	    			respStr = True
	    	elif ansObj.question.questionType == 2:
	    	    try:
		    	    if ansObj.answerGrade.lower() == validateValue.lower():
		    	        respStr = True
		    	    elif float(ansObj.answerGrade) == float(validateValue):
		    	    	respStr = True
		    except:
		    	pass
	    	else:
	    	    try:
		    	    if float(ansObj.answerScore) == float(validateValue):
		    	        respStr = True
	    	    except:
	    	    	pass
	else:
		respStr = False
    return HttpResponse(simplejson.dumps(respStr))

        
urlpatterns = patterns('', 
   url(r'^answer/data/entry/$', KLP_DataEnry),
   url(r'^answer/data/validation/$', KLP_DataValidation),
)        
