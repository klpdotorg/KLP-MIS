#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import psycopg2
from emsproduction.settings import *
import pdb
from django.db import connection
debug_mode=0

def getBoundaryRes(boundaryDict,boundaryType):
    ''' Boundary Related Queries '''
    sTime = boundaryDict['sTime']
    eTime = boundaryDict['eTime']
    userId = boundaryDict['userId']
    contId = boundaryDict['contId']
    from django.db import connection
    cursor = connection.cursor()

    #boundary created query
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time  > %s and action_time < %s and action = 'C' and content_type_id = %s and request_id in ( select id from fullhistory_request where user_pk = %s) and cast(object_id as int) in ( select id from schools_boundary where boundary_type_id = %s)",[sTime, eTime, contId, userId, boundaryType])

    res = cursor.fetchone()
    created = int(res[0])

    #boundary updated query
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time  > %s and action_time < %s and action = 'U' and content_type_id = %s and request_id in ( select id from fullhistory_request where user_pk = %s) and cast(object_id as int) in ( select id from schools_boundary where boundary_type_id = %s) and data ~* %s",[sTime, eTime, contId, userId, boundaryType, 'name'])

    res = cursor.fetchone()
    updated = int(res[0])

    #boundary deleted query
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time  > %s and action_time < %s and action = 'U' and content_type_id = %s and request_id in ( select id from fullhistory_request where user_pk = %s) and cast(object_id as int) in ( select id from schools_boundary where boundary_type_id = %s) and data ~* %s",[sTime, eTime, contId, userId, boundaryType, 'active'])

    res = cursor.fetchone()
    removed = int(res[0])
    cursor.close()
    return {'created': created, 'updated': updated, 'removed': removed}



def getInstRes(instdict, insttype):
    sTime = instdict['sTime']
    eTime = instdict['eTime']
    userId = instdict['userId']
    contId = instdict['contId']
    from django.db import connection
    cursor = connection.cursor()

    # institution created by user
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and content_type_id = %s and action = 'C' and request_id in ( select id from fullhistory_request where user_pk = %s) and cast(object_id as int) in ( select id from schools_institution where boundary_id in ( select id from schools_boundary where boundary_type_id = %s))",[sTime, eTime, contId,userId, insttype ])
    res = cursor.fetchone()
    created = int(res[0])

    # institution updated by user
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and content_type_id = %s and action = 'U' and request_id in ( select id from fullhistory_request where user_pk = %s) and not data = %s and cast(object_id as int) in ( select id from schools_institution where boundary_id in ( select id from schools_boundary where boundary_type_id = %s))",[sTime, eTime, contId, userId, '{"active": [2, 0]}', insttype ])
    res = cursor.fetchone()
    updated = int(res[0])

    # instituion removed by user
    cursor = connection.cursor()
    cursor.execute("select count(id) as count from fullhistory_fullhistory where action_time > %s and action_time < %s and request_id in (select id from fullhistory_request where user_pk =%s ) and content_type_id in ( select id from django_content_type where id=%s) and CAST(object_id AS INT)  in ( select id from schools_institution where boundary_id in ( select id from schools_boundary where boundary_type_id = %s)) and action=%s and data  = %s ",[sTime, eTime, userId, contId, insttype,'U','{"active": [2, 0]}'])
    res = cursor.fetchone()
    removed = int(res[0])
    cursor.close()
    return {'created': created, 'updated': updated, 'removed': removed}



def getStaffRes(staffdict, stafftype):
    sTime = staffdict['sTime']
    eTime = staffdict['eTime']
    userId = staffdict['userId']
    contId = staffdict['contId']
    from django.db import connection
    cursor = connection.cursor()

    # staff created query
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and content_type_id in ( select id from django_content_type where id = %s) and request_id in ( select id from fullhistory_request where user_pk = %s) and action = 'C' and cast(object_id as int) in ( select id from schools_staff where institution_id in ( select id from schools_institution where boundary_id in ( select id from schools_boundary where boundary_type_id in ( select id from schools_boundary_type where id = %s))))",[sTime, eTime, contId, userId, stafftype ])

    res = cursor.fetchone()
    created = int(res[0])

    # staff updated query
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and content_type_id in ( select id from django_content_type where id = %s) and request_id in ( select id from fullhistory_request where user_pk = %s) and action = 'U' and not data ~* %s and cast(object_id as int) in ( select id from schools_staff where institution_id in ( select id from schools_institution where boundary_id in ( select id from schools_boundary where boundary_type_id in ( select id from schools_boundary_type where id = %s))))",[sTime, eTime, contId, userId,'active', stafftype ])

    res = cursor.fetchone()
    updated = int(res[0])

    # staff removed query
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and content_type_id in ( select id from django_content_type where id = %s) and request_id in ( select id from fullhistory_request where user_pk = %s) and action = 'U' and  data = %s and cast(object_id as int) in ( select id from schools_staff where institution_id in ( select id from schools_institution where boundary_id in ( select id from schools_boundary where boundary_type_id in ( select id from schools_boundary_type where id = %s))))",[sTime, eTime, contId, userId,'{"active": [2, 0]}', stafftype ])

    res = cursor.fetchone()
    removed = int(res[0])

    cursor.close()

    return {'created': created, 'updated': updated, 'removed': removed}




def getStudentRes(studDict, studType):
    sTime = studDict['sTime']
    eTime = studDict['eTime']
    userId = studDict['userId']
    contId = studDict['contId']
    from django.db import connection
    cursor = connection.cursor()

    #student created query
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and action = 'C' and content_type_id = %s and request_id in ( select id from fullhistory_request where user_pk = %s) and cast(object_id as int) in (select child_id from schools_student where id in (select student_id from schools_student_studentgrouprelation where academic_id = 122  and student_group_id in ( select id from schools_studentgroup where institution_id in ( select id from schools_institution where boundary_id in (select id from schools_boundary where boundary_type_id = %s) ))))", [sTime, eTime, contId, userId, studType])
    res = cursor.fetchone()
    created = int(res[0])

    #student updated query
    cursor.execute("select (object_id) from fullhistory_fullhistory where action_time > %s and action_time < %s and action = 'U' and request_id in ( select id from fullhistory_request where user_pk = %s) and content_type_id = %s and revision > 2 and cast(object_id as int) in ( select child_id from schools_student where id in (select student_id from schools_student_studentgrouprelation where academic_id =122 and student_group_id in ( select id from schools_studentgroup where institution_id in ( select id from schools_institution where boundary_id in (select id from schools_boundary where boundary_type_id = %s) ) ))) group by object_id;", [sTime, eTime, userId, contId, studType])
    res = cursor.fetchall()

    if not res is None:
        updated = len(res)
    else:
        updated = 0

    #student remove query
    contIdobj = ContentType.objects.get(model = 'student')
    contId = contIdobj.id
    cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and action = 'U' and data ~* 'inactive' and content_type_id = %s and request_id in (select id from fullhistory_request where user_pk = %s) and cast(object_id as int) in ( select id from schools_student where active = 0 and id in (select student_id from schools_student_studentgrouprelation where academic_id =122 and student_group_id in ( select id from schools_studentgroup where institution_id in ( select id from schools_institution where boundary_id in (select id from schools_boundary where boundary_type_id = %s) ) )))", [sTime, eTime, contId, userId, studType])


    res = cursor.fetchone()

    removed = int(res[0])
    return {'created': created, 'updated':updated, 'removed':removed}

class Command(BaseCommand):

    """ Command To generate Data Entry Operators History in csv format."""

    def handle(self, *args, **options):

        start_date = args[00]
        end_date = args[1]
        fileName = args[2]
        scriptStartTime = datetime.datetime.now()
        print scriptStartTime
        contentList = ['boundary', 'institution', 'child', 'staff']

        if fileName and start_date and end_date:
            if 1:
                strDate = start_date.split('/')
                enDate = end_date.split('/')

                cwd = os.getcwd()
                path = '%s/logFiles/' % cwd
                if not os.path.exists(path):

                    os.makedirs(path)

                genFile = '%s/%s.csv' % (path, fileName)
                historyFile = csv.writer(open(genFile, 'wb'))

                contentdic = {}
                for k in contentList:
                    contObj = \
                        ContentType.objects.get(app_label='schools',
                            name=k)
                    contId = contObj.id
                    contentdic[k] = contId

                headerList = ['Sl.No', 'User', 'pre_boundary_created', 'pre_boundary_mod', 'pre_boundary_del', 'primary_boundary_created', 'primary_boundary_mod', 'primary_boundary_del', 'pre_sch_created', 'pre_sch_mod', 'pre_sch_del', 'primary_sch_created', 'primary_sch_mod', 'primary_sch_del', 'pre_stud_created', 'pre_stud_mod', 'pre_stud_del', 'primary_stud_created', 'primary_stud_mod', 'primary_stud_del', 'pre_teacher_created', 'pre_teacher_mod', 'pre_teacher_del', 'primary_teacher_created', 'primary_teacher_mod', 'primary_teacher_del']

                (asmDict, asmList) = ({}, [])
                qlist=[]

                sDate = datetime.date(int(strDate[2]), int(strDate[1]),
                        int(strDate[00]))
                eDate = datetime.date(int(enDate[2]), int(enDate[1]),
                        int(enDate[00]))
                sTime = datetime.datetime(
                    int(strDate[2]),
                    int(strDate[1]),
                    int(strDate[00]),
                    00,
                    00,
                    00,
                    )
                eTime = datetime.datetime(
                    int(enDate[2]),
                    int(enDate[1]),
                    int(enDate[00]),
                    23,
                    59,
                    00,
                    )
                print 'sTime=', sTime, 'eTime=', eTime


                userIdsList = FullHistory.objects.filter(action_time__range = (sTime, eTime)).only('request__user_pk').distinct().values_list('request__user_pk', flat=True)
                userIds=[]
                for i in userIdsList:
                    if not i == None:
                        userIds.append(i)
                print "\n\n UserIds: ", userIds


                asmids=Answer.objects.filter(creation_date__range=[sDate, eDate]).distinct('question__assessment').values_list('question__assessment', flat=True)
                asmids =  [int(i) for i in asmids]
                assessments = Assessment.objects.filter(active=2, id__in = asmids).distinct().only("id", "name")
                print "assessments are: ", assessments

                cursor = connection.cursor()

                # get answers ids from fh
                fullhistoryAnswers = \
                    cursor.execute("""select distinct CAST(object_id AS INT) from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and content_type_id in ( select id from django_content_type where name='%s')"""
                                    % (sTime, eTime,'answer'))
                validAns = "0 "
                for c in cursor.fetchall():
                    validAns += ", %s"%c[00] 

                user_ids = tuple(userIds)

                for assessment in assessments:
                    
                    questions = \
                        """select id from schools_question where assessment_id= %s and active= 2"""\
                         % assessment.id
                    cursor.execute(questions)
                    resq = cursor.fetchall()
                    qlist = "0 "

                    for i in resq:
                        qlist += ", %s "%(i[0])
                    answerQuery = \
                        """ select distinct id from schools_answer  where (user1_id in %s or  user2_id in %s  ) and  question_id in (%s)  and id in (%s)"""\
                         % (user_ids, user_ids, qlist,
                            validAns)
                    cursor.execute(answerQuery)

                    answersCur = cursor.fetchall()  # Answer.objects.raw(answerQuery)
                    if answersCur:
                            assessmentId = assessment.id
                            asmobj = Assessment.objects.get(id=assessmentId)
                            asmList.append(assessmentId)
                            asmName = '%s-%s' \
                                % (asmobj.programme.name,
                                   asmobj.name)
                            headerList.append("Assess Id")
                            headerList.append(asmName
                                    + ' Num Of correct Entries')
                            headerList.append(asmName
                                    + ' Num Of incorrect Entries')
                            headerList.append(asmName
                                    + ' Num Of verified Entries')
                            headerList.append(asmName
                                    + ' Num Of rectified Entries')
                            nList =  [c[00] for c in answersCur]
                            nList.append(00)
                            asmDict[assessmentId] = nList
                historyFile.writerow(headerList)

                count = 00
                users = User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'], is_active=1, id__in = userIds).order_by("username")
                if users:
                    for user in users:
                        count += 1
                        userId = user.id
                        dataList = [count, user.username]

                        for content in contentList:
                            (preList, primaryList) = ([00], [00])
                            contObj = \
                                ContentType.objects.get(app_label='schools'
                                    , name=content)
                            contId = contObj.id
                            querydict = {'sTime':sTime, 'eTime':eTime, 'userId': userId, 'contId':contId}
                            if content == 'boundary':

                                #primary boundary queries 
                                querytype = 1
                                primary_boundary = getBoundaryRes(querydict, querytype)

                                #pre boundary queries 
                                querytype = 2
                                pre_boundary = getBoundaryRes(querydict, querytype)

                            elif content == 'institution':

                                #primary instituion queries 
                                querytype = 1
                                primary_institution = getInstRes(querydict, querytype)

                                #pre instituion queries 
                                querytype = 2
                                pre_institution = getInstRes(querydict, querytype)

                            elif content == 'staff':

                                #primary staff queries 
                                querytype = 1
                                primary_staff = getStaffRes(querydict, querytype)

                                #pre staff queries 
                                querytype = 2
                                pre_staff = getStaffRes(querydict, querytype)


                            elif content == 'child':

                                #primary student queries 
                                querytype = 1
                                primary_student = getStudentRes(querydict, querytype)

                                #pre student queries 
                                querytype = 2
                                pre_student = getStudentRes(querydict, querytype)

                        dataList.append(pre_boundary['created'])
                        dataList.append(pre_boundary['updated'])
                        dataList.append(pre_boundary['removed'])

                        dataList.append(primary_boundary['created'])
                        dataList.append(primary_boundary['updated'])
                        dataList.append(primary_boundary['removed'])

                        dataList.append(pre_institution['created'])
                        dataList.append(pre_institution['updated'])
                        dataList.append(pre_institution['removed'])

                        dataList.append(primary_institution['created'])
                        dataList.append(primary_institution['updated'])
                        dataList.append(primary_institution['removed'])

                        dataList.append(pre_student['created'])
                        dataList.append(pre_student['updated'])
                        dataList.append(pre_student['removed'])

                        dataList.append(primary_student['created'])
                        dataList.append(primary_student['updated'])
                        dataList.append(primary_student['removed'])


                        dataList.append(pre_staff['created'])
                        dataList.append(pre_staff['updated'])
                        dataList.append(pre_staff['removed'])

                        dataList.append(primary_staff['created'])
                        dataList.append(primary_staff['updated'])
                        dataList.append(primary_staff['removed'])

                        for asmId in asmList:

                            answers = asmDict[asmId]
                            status = 'modifiedBy": ' + '[' + str(userId) + ',]'
                            anscttyp = ContentType.objects.get(name='answer')
                            if answers:

                                #correct entires sql
                                # Hom many answers i created for an assessment...
                                crQuery = """select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s )  and CAST(object_id AS INT)  in %s and action='C'""" % (sTime, eTime, userId, tuple(answers))
                                cursor.execute(crQuery)
                                res = cursor.fetchone()
                                crEntries = int(res[0])

                                # ids of answer records that i created for an assessment...
                                crQueryData = """select object_id as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s )  and CAST(object_id AS INT)  in %s and action='C'""" % (sTime, eTime, userId, tuple(answers))
                                cursor.execute(crQueryData)
                                res = cursor.fetchall()
                                crEntriesLis = [i[0] for i in res]
                                
                                if not crEntriesLis:
                                    crEntriesLis = [0,0]
                                crEntriesLisInt = [int(i) for i in crEntriesLis]
                                if not crEntriesLisInt:
                                    crEntriesLisInt = [0,0]

                                if crEntries == 00:
                                    inCrEntries = 00
                                else:
                                    # How many of my answers were wrong...; showing all recored, which were created by me, 
                                    # but now updated by others for an assessment.
                                    # incorrect entries sql
                                    cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and action = 'U' and not request_id in ( select id from fullhistory_request where user_pk = %s) and CAST(object_id AS INT) in %s and data ~* %s and (data ~* %s or data ~* %s ) and not (data ~* %s or data ~* %s or data ~* %s)",[sTime, eTime, userId, tuple(crEntriesLisInt),'user2','answer','status','id','question','student'])
                                    res = cursor.fetchone()
                                    inCrEntries = int(res[0])

                                # verified entries sql
                                # how many others records I verified by double entry for an assessment...
                                cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and action = 'U' and request_id in ( select id from fullhistory_request where user_pk = %s) and CAST(object_id AS INT) in %s and data ~* %s and not (data ~* %s or data ~* %s or data ~* %s or data ~* %s or data ~* %s)",[sTime, eTime, userId, tuple(answers),'user2','id','question','student','answer', 'status'])
                                res = cursor.fetchone()
                                vEntries = int(res[0])

                                # rectfied entires sql
                                # how many others wrong answers I corrected/ fixed by double entry for an assessment...
                                cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and action = 'U' and request_id in ( select id from fullhistory_request where user_pk = %s) and CAST(object_id AS INT) in %s and data ~* %s and (data ~* %s or data ~* %s ) and not (data ~* %s or data ~* %s or data ~* %s)",[sTime, eTime, userId, tuple(answers),'user2','answer','status','id','question','student'])
                                res = cursor.fetchone()
                                rEntries = int(res[0])


                                dataList.append(asmId)
                                dataList.append(crEntries)
                                dataList.append(inCrEntries)
                                dataList.append(vEntries)
                                dataList.append(rEntries)
                        historyFile = csv.writer(open(genFile, 'a'
                            ))
                        historyFile.writerow(dataList)
                        print "\nuserId " + str(userId) + " is processed"
                print '%s.csv file has been created in %s/logFiles directory' % (fileName, cwd)
                print 'Time taken: %s' %(datetime.datetime.now() - scriptStartTime)
            else:
                pass
            cursor.close()
        else:
            raise CommandError('Pass Startdate, end date and filename.\n')
