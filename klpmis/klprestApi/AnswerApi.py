#!/usr/bin/python
# -*- coding: utf-8 -*-

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
from django.db import IntegrityError
from schools.receivers import KLP_obj_Perm
import pdb

from django.forms.models import modelformset_factory

def KLP_DataEnry(request):
    return HttpResponse(KLP_ChangeAns(permitted_methods=('POST', 'GET'
                        )).read(request))


class KLP_ChangeAns(Resource):

    """ To Create and Edit Answers answer/data/entry/"""

    def read(self, request):

        user = request.user  # get Logged in user
        userid = user.id
        student = request.POST.get('student')  #  get Student
        programId = request.POST.get('programId')  #  get programme id
        assessmentId = int(request.POST.get('assessmentId'))  # get Assessment Id

        # assessmentObj1=Assessment.objects.filter(pk=assessmentId).defer("programme")

        assessmentObj = Assessment.objects.get(pk=assessmentId)
        student_groupId = request.POST.get('student_groupId')  #  get Student group id
        student_groupObj = \
            StudentGroup.objects.filter(pk=student_groupId).defer('institution'
                )
        
        if assessmentObj.typ == 3:
            modelName='student'
            student_groupObj = student_groupObj.values('institution')[0]  # get SG Object based on id
            instObj = \
                Institution.objects.filter(pk=student_groupObj['institution'
                    ]).defer('boundary', 'cat', 'mgmt', 'inst_address'
                             )[0]  # get Institution Object based on id
             
            studentObj1 = Student.objects.filter(id=student.split('_')[0]).defer('child')

           # childObj=studentObj1.defer("child")[0]

            studentObj = studentObj1[0]
        elif assessmentObj.typ == 2:
            modelName='studentgroup' 
            studentObj = student_groupObj[0]
            instObj = studentObj.institution
        
        else:
            modelName='institution'
            instObj = \
                Institution.objects.filter(pk=student_groupId).defer('boundary'
                    , 'cat', 'mgmt', 'inst_address')
            studentObj = instObj[0]
        Questions_list = \
            Question.objects.filter(assessment__id=assessmentId)  # get questions under assessment
        dobleEntReq = assessmentObj.double_entry
        
        if dobleEntReq:
            dE = 2 
        else:
            dE = 1 

        # Checking user permission based on institution and assessment

        KLP_obj_Perm(user, instObj, 'Acess', assessmentObj)
        studentObjid = studentObj.id
        rowcounter = request.POST.get('rowcounter')
        cTObj=ContentType.objects.get(name=modelName)
        ansIds=[]
        for (index, question) in enumerate(Questions_list):
            textField = 'student_%s_%s' % (str(question.id), student)
            textFieldVal = request.POST.get(textField)  # get each text field values
            
            primaryfield = 'primaryvalue_%s' % student
            primaryfieldVal = request.POST.get(primaryfield, '')
            ansIdfield = 'ansId_%s_%s' % (str(question.id), student)
            ansIdfieldVal = 0 if request.POST.get(ansIdfield, '') in [ None,'None'] else request.POST.get(ansIdfield, '')

        
        
            ansObjs = []
            # If answer object already exists update data.
            if ansIdfieldVal:
                ansObjs=Answer.objects.filter(id=ansIdfieldVal)
            try:
                ansObj =ansObjs[0]  # .defer("user1","user2")[0]
            except:

                ansObj = ''
        
            
            #AnswerForm= modelformset_factory(Answer,form=Answer_Form,extra=0)
            newanswerdata=request.POST.copy()
            AnswerForm= modelformset_factory(Answer,form=Answer_Form)
            if ansObj:
                ansObj.flexi_data = primaryfieldVal
                newanswerdata['form-0-flexi_data']=primaryfieldVal
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
        
        
                        ansScore = 0
                        if ansObj.answer_score:
                            ansScore = '%.2f' \
                                % float(ansObj.answer_score)
                        textScore = '%.2f' % float(textFieldVal)
                        if ansScore != textScore:
                            ansObj.answer_score = textFieldVal
                    user1 = ansObj.user1
                    user1id = user1.id
        
                    if ansObj.double_entry == 1 and user1id == userid :

                        # if the double_entry value for answer is 1(only first user enter data) and user1 is same as logged in user change last_modified_by to current user

                        ansObj.last_modified_by = user1
                    else:

                    # else update double_entry to 2(second user also submits data), last_modified_by and user2 to logged user

                        ansObj.double_entry = 2
                        ansObj.last_modified_by = user
                        ansObj.user2 = user
                    
                    try:
                        
                        newanswerdata['form-0-answer_score']=ansObj.answer_score
                        newanswerdata['form-0-last_modified_by']=ansObj.last_modified_by.id
                        #newanswerdata['form-0-answerText']=ansObj.answerText
                        newanswerdata['form-0-double_entry']=ansObj.double_entry
                        newanswerdata['form-0-status']=ansObj.status
                        newanswerdata['form-0-answer_grade']=ansObj.answer_grade
                        newanswerdata['form-0-question']=question.id
                        newanswerdata['form-0-content_type']=cTObj.id
                        newanswerdata['form-0-object_id']=studentObj.id
                        newanswerdata['form-0-active']=2  
                        newanswerdata['form-0-user1']=ansObj.user1.id
                        if ansObj.user2:
                            newanswerdata['form-0-user2']=ansObj.user2.id #.id
                        else:
                            newanswerdata['form-0-user2']=''
                        
                        newanswerdata['form-0-id']=ansObj.id  
                        newanswerdata['form-INITIAL_FORMS']=1

                        request.POST=newanswerdata

                        firstuserdata1 = Answer.objects.filter(question__id=\
                        question.id, user1__id = user.id, object_id = \
                        studentObj.id,id=ansObj.id)

                        ansflexivals = Answer.objects.filter(question__id=\
                        question.id, object_id = \
                        studentObj.id,flexi_data = ansObj.flexi_data)

                        ansForm=AnswerForm(request.POST,request,queryset=ansObjs)
                        if not firstuserdata1.count() == 0:
                            f1 = firstuserdata1[0]
                            if f1.flexi_data != primaryfieldVal and not ansflexivals:
                                f1.answer_score = ansObj.answer_score
                                f1.answer_grade = ansObj.answer_grade
                                f1.flexi_data = ansObj.flexi_data
                                f1.save()
                            elif f1 and f1.flexi_data == primaryfieldVal:
                                f1.answer_score = ansObj.answer_score
                                f1.answer_grade = ansObj.answer_grade
                                f1.save()
                            else:
                                return 'Primary Value is already existing  '
                        else:
                            if ansForm.errors:
                               if ansForm.errors[0].has_key('__all__'):
                                  return 'Primary Value is already existing  '
                            ansForm.save()
                        #ansObj.save()  # Save Answer object
                    except IntegrityError:
                        return 'Primary Value is already existing  '
            else:

        
                if textFieldVal:

                    # If Answer object not exists create new answer object

                    (status, answer_grade, answer_score) = (None, None,                           None)
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
        
                    if dE==2 :
                        d_entry=1
                    else:
                       d_entry=2      
                    ansObj = Answer(
                        question=question,
                        flexi_data=primaryfieldVal,
                        content_object=studentObj,
                        double_entry=d_entry,
                        status=status,
                        answer_grade=answer_grade,
                        answer_score=answer_score,
                        last_modified_by=user,
                        user1=user,
                        )

                    # ansObj = Answer(question=question, content_type = cTObj, object_id = savId, double_entry=dE, status=status, answer_grade=answer_grade, answer_score=answer_score, answerText=answerText, last_modified_by=user, user1=user)................

                    try:
                        newanswerdata['form-0-answer_score']=answer_score
                        newanswerdata['form-0-last_modified_by']=user.id
                        newanswerdata['form-0-flexi_data']=primaryfieldVal
                        newanswerdata['form-0-double_entry']=d_entry
                        newanswerdata['form-0-status']=status
                        newanswerdata['form-0-answer_grade']=answer_grade

                        newanswerdata['form-0-user1']=user.id
                        newanswerdata['form-0-question']=question.id
                        newanswerdata['form-0-content_type']=cTObj.id
                        newanswerdata['form-0-object_id']=studentObj.id


                        firstuserdata = Answer.objects.filter(question__id=\
                        question.id, user1__id = user.id, object_id = \
                        studentObj.id, flexi_data = primaryfieldVal)

                        ansflexivals2 = Answer.objects.filter(question__id=\
                        question.id, object_id = \
                        studentObj.id,flexi_data = primaryfieldVal)
                        
                        try:
                            fdata = Answer.objects.get(question__id=question.id,\
                        object_id = studentObj.id, flexi_data = primaryfieldVal)
                        except:
                            fdata=''
                        if not firstuserdata.count() == 0:
                            f =  firstuserdata[0]
                            f.answer_score = answer_score
                            f.answer_grade = answer_grade
                            f.save()
                            

                        else:
                            ansForm=AnswerForm(newanswerdata,request)


                            if ansForm.errors:
                                if ansForm.errors[0].has_key('__all__'):
                                  return 'Primary Value is already existing  '
                            
                            ansForm.save()
                            

                        #ansObj.save()
                    except IntegrityError:
                        return 'Primary  Value is already existing'
            try:
                ansIds.append(str(ansObj.id))      
            except:
                pass
        return 'Data(s) Saved |'+','.join(ansIds)  # ,question.id,',',studentObj.id,',',dE,',',status,',',answer_grade,answer_score,user.id




def KLP_DataValidation(request):
    """ To Validate data for Doble Entry answer/data/validation/"""
    
    validateId = request.POST.get('validateField')  #  Get ValidateId (student and question id)
    validateValue = request.POST.get('validateValue')  #  Get Text field value to validate
    listIds = validateId.split('_')
    AnsId=request.POST.get('ansId')
    # Query Answer object based on student and question id
    print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", AnsId
    if AnsId != "None":
       ansObj=Answer.objects.filter(id=AnsId).defer('object_id'
            , 'user1', 'user2', 'last_modified_by')[0]
    else: 
      ansObj = Answer.objects.filter(object_id=listIds[2],
                                   question__id=listIds[1]).defer('object_id'
            , 'user1', 'user2', 'last_modified_by')
      if ansObj:
          ansObj=ansObj[0]
    respStr = False
    if ansObj:
        dEntry = int(ansObj.double_entry)  # reads dE value
        
        if dEntry in [0, 2]:

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
                    if 1:

                            # If question type is 2(Grade) then match with answer grade if matches return true

                        if ansObj.answer_grade.lower() \
                            == validateValue.lower():
                            respStr = True
                        elif (ansObj.answer_grade) == (validateValue):
                            respStr = True
                    else:
                        pass
                else:
                    if 1:

                            # If question type is 1(marks) then match with answer score if matches return true
                        

                        if float(ansObj.answer_score) \
                            == float(validateValue):
                            respStr = True
                    else:
                        pass
            else:
                respStr = False
    else:
        pass
    return HttpResponse(simplejson.dumps(respStr))

def KLP_getAnswers(request):
    resp=False
    aid = request.GET.get('aid')  #  Get Assessment id
    obid = request.GET.get('obid')
    print "Assessment id", aid
    try:
        asobj = Answer.objects.filter(object_id=obid,question__assessment__id=aid)
    except:
        asobj = ''
    print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", resp
    if asobj:
        resp = True
    else:
        pass
    return HttpResponse(simplejson.dumps(resp))


urlpatterns = patterns('', url(r'^answer/data/entry/$', KLP_DataEnry),
                       url(r'^answer/data/validation/$',
                       KLP_DataValidation),
                       url(r'^klp/getanswers/$',KLP_getAnswers)
                       )
