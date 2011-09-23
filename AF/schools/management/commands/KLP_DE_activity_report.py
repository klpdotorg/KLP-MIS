from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from django.contrib.contenttypes.models import ContentType
from fullhistory.models import FullHistory
from django.db.models import Q 
from django.contrib.auth.models import User
import django
import datetime
import os
import csv

class Command(BaseCommand):
    ''' Command To generate Data Entry Operators History in csv format. 
    Takes filename, startDate, endDate as input parameters.
    A csv file will be created as output in a subfolder called logfiles in current folder.'''

    def handle(self, *args, **options):
        if 1: #try:
            # read start date, end date and filename
            startDate = args[0]
            endDate = args[1]
            fileName = args[2]
            contentTypeIds = {}
            ## Create a dictionary of valid content types
            for modelType in ContentType.objects.filter(app_label='schools'):
                contentTypeIds[modelType.model]=modelType.id
        
            if fileName and startDate and endDate:
                if 1: #try:
                    strDate = startDate.split("/")
                    enDate = endDate.split("/")
                    sDate = datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0]))
                    eDate = datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0]))
                    sTime = datetime.datetime(int(strDate[2]), int(strDate[1]), int(strDate[0]), 00, 00, 00)
                    eTime = datetime.datetime(int(enDate[2]), int(enDate[1]), int(enDate[0]), 23, 59, 00)
                    
                    # get current working directory.
                    cwd = os.getcwd()
                    path = "%s/logFiles/" %(cwd)
                    if not os.path.exists(path):# if dir not exists creates directory with name logfiles in cwd.
                        os.makedirs(path)
                    genFile = "%s/%s.csv" %(path, fileName)# create csv file with the name passed.        
                    historyFile = csv.writer(open(genFile, 'wb'))
                    # Write header
                    headerList = ['Sl.No', 'User', 'pre_boundary_created', 'pre_boundary_modified', 'pre_boundary_deleted', 'primary_boundary_created', 'primary_boundary_modified', 'primary_boundary_deleted', 'pre_sch_created', 'pre_sch_modified', 'pre_sch_deleted', 'primary_sch_created', 'primary_sch_modified', 'primary_sch_deleted', 'pre_stud_created', 'pre_stud_modified', 'pre_stud_deleted', 'primary_stud_created', 'primary_stud_modified', 'primary_stud_deleted', 'pre_teacher_created', 'pre_teacher_modified', 'pre_teacher_deleted', 'primary_teacher_created', 'primary_teacher_modified', 'primary_teacher_deleted','answer_entered','answer_wrong','answer_verified','answer_rectified']
                    
                    
                    
                    validFullHistoryRecords = FullHistory.objects.filter(action_time__range=(sTime, eTime) )
                    validUserIds = validFullHistoryRecords.only('request__user_pk').distinct().values_list('request__user_pk', flat=True)
                    
                    users = User.objects.filter(is_active=1).order_by("username").only("id", "username").filter(id__in=validUserIds)
                    userIds = users.values_list("id", flat=True)
                    
                    answersUpdatedStrList = validFullHistoryRecords.filter( content_type__id=contentTypeIds['answer']).only('object_id').distinct().values_list('object_id',flat=True)
                
                    answersUpdatedList =[]
                    for item in answersUpdatedStrList:
                        answersUpdatedList.append(int(item))
                    assessmentsInvolvedInReport = Question.objects.filter(id__in=Answer.objects.filter(id__in=answersUpdatedList).only('question__id').distinct().values_list('question__id', flat=True)).only('assessment__id').distinct().values_list('assessment__id', flat=True)
                    
                    
                    for assessmentId in assessmentsInvolvedInReport:
                        headerList.append(str(assessmentId)+'_created')
                        headerList.append(str(assessmentId)+'_verified')
                        headerList.append(str(assessmentId)+'_rectified')
                    historyFile.writerow(headerList)
                    
                    for i,user in enumerate(users):
                        pre_boundary_created = 0
                        pre_boundary_modified = 0
                        pre_boundary_deleted = 0
                        primary_boundary_created = 0
                        primary_boundary_modified = 0
                        primary_boundary_deleted = 0
                        pre_sch_created = 0
                        pre_sch_modified = 0
                        pre_sch_deleted = 0
                        primary_sch_created = 0
                        primary_sch_modified = 0
                        primary_sch_deleted = 0
                        pre_stud_created = 0
                        pre_stud_modified = 0
                        pre_stud_deleted = 0
                        primary_stud_created = 0
                        primary_stud_modified = 0
                        primary_stud_deleted = 0
                        pre_teacher_created = 0
                        pre_teacher_modified = 0
                        pre_teacher_deleted = 0
                        primary_teacher_created = 0
                        primary_teacher_modified = 0
                        primary_teacher_deleted = 0
                        answer_entered = 0
                        answer_wrong = 0
                        answer_verified = 0
                        answer_rectified = 0
                        assessmentsModified ={}
                        
                        
                        ################################ Objects of type Boundary, School, Teacher, Student
                        #  C => Content created
                        #  U + data contains "active: '[2,   => Content modified and status changed from active-state to non-active states(deleted!)
                        #  U + data DOES-NOT contain "active: '[, => content updated and is still in active state!
                        #
                        ################################
                        
                        boundariesUpdatedByUserStrList = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['boundary']).only('object_id').values_list('object_id',flat=True)
                        boundariesUpdatedByUser =[]
                        for item in boundariesUpdatedByUserStrList:
                            boundariesUpdatedByUser.append(int(item))
                        
                        if boundariesUpdatedByUser:
                            preSchoolBoundaries = Boundary.objects.filter(id__in=boundariesUpdatedByUser,boundary_type__id=2).only('id').values_list('id',flat= True)
                            if preSchoolBoundaries:
                                preSchoolBoundaries = ['%s' %i for i in preSchoolBoundaries]
                                pre_boundary_created = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['boundary'], object_id__in=preSchoolBoundaries, action='C').count()
                                pre_boundary_modified = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['boundary'], object_id__in=preSchoolBoundaries, action='U').exclude(_data__contains="'active': [2,").count()
                                pre_boundary_deleted = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['boundary'],  object_id__in=preSchoolBoundaries, action='U',_data__contains='"active": [2,').count()
                            
                            primarySchoolBoundaries = Boundary.objects.filter(id__in=boundariesUpdatedByUser,boundary_type__id=1).only('id').values_list('id',flat= True)
                            if primarySchoolBoundaries:
                                primarySchoolBoundaries = ['%s' %i for i in primarySchoolBoundaries]
                                primary_boundary_created = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['boundary'],  object_id__in=primarySchoolBoundaries, action='C').count()
                                primary_boundary_modified =  validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['boundary'], object_id__in=primarySchoolBoundaries, action='U').exclude(_data__contains="'active': [2,").count()
                                primary_boundary_deleted =  validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['boundary'], object_id__in=primarySchoolBoundaries, action='U', _data__contains="'active': [2,").count() 
                        

                        schoolsUpdatedByUserStrList = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['institution']).only('object_id').values_list('object_id',flat=True)
                        
                        schoolsUpdatedByUser =[]
                        for item in schoolsUpdatedByUserStrList:
                            schoolsUpdatedByUser.append(int(item))
                        
                        if schoolsUpdatedByUser:
                            preSchools = [str(school) for school in Institution.objects.filter(id__in=schoolsUpdatedByUser,boundary__boundary_type__id=2).only('id').values_list('id',flat= True)]
                            if preSchools:
                                pre_sch_created = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['institution'], object_id__in=preSchools, action='C').count()
                                pre_sch_modified = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['institution'], object_id__in=preSchools, action='U').exclude(_data__contains="'active': [2,").count()
                                pre_sch_deleted = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['institution'],  object_id__in=preSchools, action='U',_data__contains="'active': [2,").count()
                            
                            primarySchools = [str(school) for school in Institution.objects.filter(id__in=schoolsUpdatedByUser,boundary__boundary_type__id=1).only('id').values_list('id',flat= True)]
                            if primarySchools:
                                primary_sch_created = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['institution'],  object_id__in=primarySchools, action='C').count()
                                primary_sch_modified =  validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['institution'], object_id__in=primarySchools, action='U').exclude(_data__contains="'active': [2,").count()
                                primary_sch_deleted =  validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['institution'], object_id__in=primarySchools, action='U', _data__contains="'active': [2,").count() 
                        

                        studentsUpdatedByUserStrList = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['student']).only('object_id').values_list('object_id',flat=True)
                        
                        studentsUpdatedByUser =[]
                        for item in studentsUpdatedByUserStrList:
                            studentsUpdatedByUser.append(int(item))
                            
                        if studentsUpdatedByUser:
                            preSchoolStudents = [str(student) for student in Student_StudentGroupRelation.objects.filter(student__id__in=studentsUpdatedByUser, student_group__group_type='Centre').only('student_id').values_list('student_id',flat=True)]
                            if preSchoolStudents:
                                preSchoolStudents = ['%s' %i for i in preSchoolStudents]
                                pre_stud_created = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['child'], object_id__in=preSchoolStudents, action='C').count()
                                pre_stud_modified = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['child'], object_id__in=preSchoolStudents, action='U').exclude(_data__contains="'active': [2,").count()
                                pre_stud_deleted = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['child'],  object_id__in=preSchoolStudents, action='U',_data__contains="'active': [2,").count()
                            
                            primarySchoolStudents = [str(student) for student in Student_StudentGroupRelation.objects.filter(student__id__in=studentsUpdatedByUser, student_group__group_type='Class').only('student_id').values_list('student_id',flat=True)]
                            if primarySchoolStudents:
                                primarySchoolStudents = ['%s' %i for i in primarySchoolStudents]
                                primary_stud_created = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['child'],  object_id__in=primarySchoolStudents, action='C').count()
                                primary_stud_modified =  validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['child'], object_id__in=primarySchoolStudents, action='U').exclude(_data__contains="'active': [2,").count()
                                primary_stud_deleted =  validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['child'], object_id__in=primarySchoolStudents, action='U', _data__contains="'active': [2,").count()                 
                

                        teachersUpdatedByUserStrList = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['staff']).only('object_id').values_list('object_id',flat=True)
                        teachersUpdatedByUser = []
                        for item in teachersUpdatedByUserStrList:
                            teachersUpdatedByUser.append(int(item))
                        
                        if teachersUpdatedByUser:
                            preSchoolTeachers = [str(teacher) for teacher in Staff.objects.filter(id__in=teachersUpdatedByUser, institution__boundary__boundary_type__id=2)]
                            if preSchoolTeachers:
                                pre_techer_created = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['staff'], object_id__in=preSchoolTeachers, action='C').count()
                                pre_teacher_modified = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['staff'], object_id__in=preSchoolTeachers, action='U').exclude(_data__contains="'active': [2,").count()
                                pre_teacher_deleted = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['staff'],  object_id__in=preSchoolTeachers, action='U',_data__contains="'active': [2,").count()
                            
                            primarySchoolTeachers = [str(teacher) for teacher in Staff.objects.filter(id__in=studentsUpdatedByUser, institution__boundary__boundary_type__id=2)]
                            if primarySchoolTeachers:
                                primary_teacher_created = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['staff'],  object_id__in=primarySchoolTeachers, action='C').count()
                                primary_teacher_modified =  validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['staff'], object_id__in=primarySchoolTeachers, action='U').exclude(_data__contains="'active': [2,").count()
                                primary_teacher_deleted =  validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['staff'], object_id__in=primarySchoolTeachers, action='U', _data__contains="'active': [2,").count()     
                
                
                        answersUpdatedByUserStr = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['answer']).only('object_id').values_list('object_id',flat=True)
                        answersUpdatedByUser = []
                        for item in answersUpdatedByUserStr:
                            answersUpdatedByUser.append(int(item))
                        
                        ################################ Objects of type Answer
                        #  C+ request__user_pk=user.id  =>Content created by user
                        #  U + request 
                        #  U + data DOES-NOT contain "active: '[, => content updated and is still in active state!
                        #
                        ################################
                        
                        if answersUpdatedByUser:
                            for assessmentId in assessmentsInvolvedInReport:
                                answersUpdatedForGivenAssessmentInt = Answer.objects.filter(question__in=Question.objects.filter(assessment__id=assessmentId), id__in=answersUpdatedByUser).only('id').values_list('id',flat=True)
                                answersUpdatedForGivenAssessment =[]
                                for item in answersUpdatedForGivenAssessmentInt:
                                    answersUpdatedForGivenAssessment.append(str(item))
                                answer_entered = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['answer'], object_id__in=answersUpdatedForGivenAssessment, action='C').count() #Hom many answers i created...
                                assessmentsModified[str(assessmentId)+'_entered']=   answer_entered
                                
                                answerEnteredIds = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['answer'], object_id__in=answersUpdatedForGivenAssessment, action='C').only('object_id').values_list('object_id', flat=True) # ids of answer records that i created
                                
                                
                                answer_verified = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['answer'], object_id__in=answersUpdatedForGivenAssessment, action='U' ).exclude(object_id__in=answerEnteredIds, _data__icontains='answer').count()#how many others records I verified by double entry
                                assessmentsModified[str(assessmentId)+'_verified']=   answer_verified
                                
                                
                                answer_rectified = validFullHistoryRecords.filter(request__user_pk=user.id, content_type__id=contentTypeIds['answer'], object_id__in=answersUpdatedForGivenAssessment, action='U',_data__icontains='answer' ).exclude(object_id__in=answerEnteredIds).count()#how many others wrong answers I corrected/ fixed by double entry
                                assessmentsModified[str(assessmentId)+'_rectified']=   answer_rectified
                                
                            answer_wrong =  validFullHistoryRecords.filter( content_type__id=contentTypeIds['answer'],  action='U', _data__contains='modifiedBy": ['+str(user.id)+', ', _data__icontains='answer').exclude(request__user_pk=user.id).count()     #How many of my answers were wrong...; showing all recored, which were created by me, but now updated by others.
                    
                    
                
                        # Written data into file.
                        dataList = [i,user.username, pre_boundary_created, pre_boundary_modified, pre_boundary_deleted, primary_boundary_created, primary_boundary_modified, primary_boundary_deleted, pre_sch_created, pre_sch_modified, pre_sch_deleted, primary_sch_created, primary_sch_modified, primary_sch_deleted, pre_stud_created, pre_stud_modified, pre_stud_deleted, primary_stud_created, primary_stud_modified, primary_stud_deleted, pre_teacher_created, pre_teacher_modified, pre_teacher_deleted, primary_teacher_created, primary_teacher_modified, primary_teacher_deleted, answer_entered, answer_wrong, answer_verified, answer_rectified]
                        for assessmentId in assessmentsInvolvedInReport:
                            dataList.append(assessmentsModified.get(str(assessmentId)+'_created',0))
                            dataList.append(assessmentsModified.get(str(assessmentId)+'_verified',0))
                            dataList.append(assessmentsModified.get(str(assessmentId)+'_rectified',0))
                            
                        historyFile.writerow(dataList)                                                            
                    print "%s.csv file has been created in %s/logFiles directory" %(fileName, cwd)
                else: #except IndexError: # if arguments are not proper raises an command error.
                    pass #raise CommandError('Date Should be in dd/mm/yyyy format.\n')
            else:
                print "need parameters fileName, startDate and endDate - use dd/mm/yyyy "
        else: #except:
            print "need parameters fileName, startDate and endDate - use dd/mm/yyyy "

