""" AnswerApi file is used to store answers entered by data entry operators And also do validation while double entry"""

from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry
from django.template import Template, Context, RequestContext
from schools.forms import *
from schools.models import *
from django_restapi.authentication import *

from schools.receivers import KLP_obj_Perm
         
def KLP_DataEnry(request):
        return HttpResponse(KLP_ChangeAns(permitted_methods=('POST','GET')).read(request))
        
        
class KLP_ChangeAns(Resource):
    """ To Create and Edit Answers answer/data/entry/"""
    def read(self,request):
    	user = request.user # get Logged in user
        userid=user.id
        student =  request.POST.get('student')    #  get Student 
        programId = request.POST.get('programId') #  get programme id
        assessmentId = int(request.POST.get('assessmentId')) # get Assessment Id
        #assessmentObj1=Assessment.objects.filter(pk=assessmentId).defer("programme")
        assessmentObj= Assessment.objects.get(pk=assessmentId)
        student_groupId = request.POST.get('student_groupId') #  get Student group id
        student_groupObj=StudentGroup.objects.filter(pk = student_groupId).defer('institution')
        print student_groupObj
        if assessmentObj.typ==3:
           student_groupObj = student_groupObj.values("institution")[0]  # get SG Object based on id
           instObj = Institution.objects.filter(pk=student_groupObj["institution"]) .defer("boundary","cat","mgmt","inst_address")[0]  # get Institution Object based on id
           studentObj1 = Student.objects.filter(pk=student).defer("child")
           #childObj=studentObj1.defer("child")[0]
           studentObj=studentObj1[0] 
        elif assessmentObj.typ==2:
          studentObj=student_groupObj[0]
          instObj =studentObj.institution
          print studentObj,'SSSSSSSSSSSSSSSSSSSSSSSss'
        else:
                          instObj= Institution.objects.filter(pk=student_groupId).defer("boundary","cat","mgmt","inst_address")
                          studentObj=instObj[0]
        Questions_list = Question.objects.filter(assessment__id=assessmentId)  # get questions under assessment
        dobleEntReq = assessmentObj.douple_entry
        if dobleEntReq:
        	dE = 1
        else:
        	dE = 2
        #Checking user permission based on institution and assessment
        KLP_obj_Perm(user, instObj, "Acess", assessmentObj)
        studentObjid=studentObj.id
        print Questions_list,'RRRRRRRRRRrrrrrrrrrrrrr'
        for question in Questions_list:
        	textField = 'student_%s_%s' %(student, str(question.id))        	
        	textFieldVal = request.POST.get(textField)  # get each text field values
        	# If answer object already exists update data.
                try:
        	  ansObj = Answer.objects.filter(question= question,object_id = studentObjid)[0] #.defer("user1","user2")[0]
                except:
                   ansObj=''
                print ansObj,'aaaaaaaaaaaaa'
                if ansObj:
        		if textFieldVal:
        			if textFieldVal.lower() == 'ab':
        				# If text field value is ab(absent) then change answer_grade and answer_score to none and status to -99999
        				ansObj.answer_grade = None
        				ansObj.answer_score = None
        				ansObj.status = -99999
        			elif textFieldVal.lower() == 'uk':
        				# If text field value is uk(unknown) then change answer_grade and answer_score to none and status to -1
        				ansObj.answer_grade = None
        				ansObj.answer_score = None
        				ansObj.status = -1
        			elif question.question_type == 2:
        				# else question type is 2(Grade) then change status to none and store textfield value in answer_grade
        				ansObj.status = None
        				ansGrade = textFieldVal
        				try:
        					ansGrade = textFieldVal.upper()
        				except:
        					pass
        				ansObj.answer_grade = ansGrade
        			elif question.question_type == 3:	
        				ansObj.answerText = textFieldVal
        			else:
        				# else question type is 1(Marks) then change status to none and store textfield value in answer_score
        				ansObj.status = None	
                                        print ansObj.answer_score,ansObj.id,'wwwwwwwwww'
                                        ansScore=0
                                        if ansObj.answer_score:
        				  ansScore = '%.2f' %(float(ansObj.answer_score))
        				textScore = '%.2f' %(float(textFieldVal))
        				if ansScore != textScore:
        					ansObj.answer_score = textFieldVal
        		        user1=ansObj.user1
                                user1id=user1.id
                                print user1,user.id 			
        			if ansObj.douple_entry == 1  and user1id == userid:
        				# if the douple_entry value for answer is 1(only first user enter data) and user1 is same as logged in user change last_modified_by to current user
					ansObj.last_modified_by = user1
                                        
				else:
					# else update douple_entry to 2(second user also submits data), last_modified_by and user2 to logged user
					ansObj.douple_entry = 2
					ansObj.last_modified_by = user
				       	ansObj.user2 = user
        			ansObj.save()	# Save Answer object
                               
        	else :
                        print textFieldVal
        		if textFieldVal:
        			# If Answer object not exists create new answer object
        			status, answer_grade, answer_score=None, None, None
        			if textFieldVal.lower() == 'ab':
					# If text field value is ab(absent) then set status to -99999
					status = -99999
				elif textFieldVal.lower() == 'uk':
					# If text field value is uk(unknown) then set status to -1
					status = -1
				elif question.question_type == 2:
					# else if  question type is 2(Grade) then store textfield value in answer_grade
        				answer_grade = textFieldVal
        				try:
        					answer_grade = textFieldVal.upper()
        				except:
        					pass
        			else:
        				# else if  question type is 1(Marks) then store textfield value in answer_score
        				answer_score = textFieldVal
			        print question.id,studentObj ,'************' #[0],studentObj[0].id,dE,status,answer_grade,answer_score,user.id,'*******'
                                ansObj = Answer(question=question, content_object=studentObj, douple_entry=dE, status=status, answer_grade=answer_grade, answer_score=answer_score, last_modified_by=user, user1=user)
                                #ansObj = Answer(question=question, content_type = cTObj, object_id = savId, douple_entry=dE, status=status, answer_grade=answer_grade, answer_score=answer_score, answerText=answerText, last_modified_by=user, user1=user)				
        			ansObj.save()
	       
	return "Data(s) Saved" #,question.id,',',studentObj.id,',',dE,',',status,',',answer_grade,answer_score,user.id


def KLP_DataValidation(request):
    """ To Validate data for Doble Entry answer/data/validation/"""
    validateId = request.POST.get('validateField')  #  Get ValidateId (student and question id)
    validateValue = request.POST.get('validateValue')  #  Get Text field value to validate
    listIds = validateId.split('_')   
    # Query Answer object based on student and question id
    ansObj = Answer.objects.filter(object_id=listIds[1], question__id=listIds[2]).defer("object_id","user1", "user2", "last_modified_by")[0]    
    respStr = False
    dEntry = int(ansObj.douple_entry)  # reads dE value
    if dEntry in [0,2]:
        # if dEntry in 0 0r 2 return true
    	respStr = True
    else:
    	# else check text field value
    	if validateValue:    		
	    	if validateValue.lower() == 'ab':
	    		# If text field value is ab(absent) and answer status is -99999 then return true
	    		if ansObj.status == -99999:
	    			respStr = True
	    	elif validateValue.lower() == 'uk':
	    		# If text field value is uk(unknown) and answer status is -1 then return true
	    		if ansObj.status == -1:
	    			respStr = True
	    	elif ansObj.question.question_type == 2:	    	
	    	    try:
	    	    	    # If question type is 2(Grade) then match with answer grade if matches return true
		    	    if ansObj.answer_grade.lower() == validateValue.lower():
		    	        respStr = True
		    	    elif float(ansObj.answer_grade) == float(validateValue):
		    	    	respStr = True
		    except:
		    	pass
	    	else:
	    	    try:
	    	    	    # If question type is 1(marks) then match with answer score if matches return true
		    	    if float(ansObj.answer_score) == float(validateValue):
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
