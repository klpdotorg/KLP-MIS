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

def get_boundary_type(preboundarytypeId,btid):
    cursor = connection.cursor()
    preboundarytypeId = \
                    """select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%d)""" % (btid)
    cursor.execute(preboundarytypeId)
    return [c[00] for c in cursor.fetchall()]

def institution_query(cid):
    catList="in (11,10,12)"
    if cid==1:
        catList="not %s" % catList
    cursor = connection.cursor()
    query = \
"""SELECT distinct id from schools_institution where cat_id in (select id from schools_institution_category where category_type %s)""" % (catList)
    return query

def get_schoolIDs(preSchoolIds,fullhistoryQuery):
    slist = \
"""select distinct student_id  from schools_Student_StudentGroupRelation where student_group_id in (select id from schools_studentgroup where institution_id in  %s ) and student_id %s  """\
                                 % (preSchoolIds, fullhistoryQuery)
    return slist


def fhquery(qd):
    q = """select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id not in (select id from fullhistory_request where user_pk =%s )  and CAST(object_id AS INT)  in %s and action='U' and (data ~* 'anwsers' or data ~* 'status' or data ~* 'user2') and request_id  not in (select id from fullhistory_request where user_pk =%s )""" \
                                     % (qd['sTime'], qd['eTime'], qd['userId'], qd['answers'], qd['userId'])
    return q

def fhrquery(rd):
    q = """select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and CAST(object_id AS INT)  in %s and action='U' and (data like '%%anwsers%%' or data like '%%status%%' or data like '%%user2%%') and request_id  not in (select id from fullhistory_request where user_pk =%s )  and (data not like '%%id%%' or data not like '%%question%%' or data not like '%%student%%')"""\
                                 % (rd['sTime'], rd['eTime'], rd['userId'], rd['answers'],rd['userId'])
    return q



class Command(BaseCommand):

    """ Command To generate Data Entry Operators History in csv format."""

    def handle(self, *args, **options):

        start_date = args[00]
        end_date = args[1]
        fileName = args[2]
        scriptStartTime = datetime.datetime.now()
        print scriptStartTime
        contentList = ['boundary', 'institution', 'student', 'staff']

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
                users = \
                    User.objects.filter(is_active=1).order_by('username'
                        ).only('id', 'username')
                userIds = users.values_list('id', flat=True)
                
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
                assessments = Assessment.objects.filter(active=2).distinct().only("id", "name")
                cursor = connection.cursor()
                fullhistoryAnswers = \
                    cursor.execute("""select distinct CAST(object_id AS INT) from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and content_type_id in ( select id from django_content_type where name='%s')"""
                                    % (sTime, eTime,'answer'))
                validAns = "0 "
                for c in cursor.fetchall():
                    validAns += ", %s"%c[00] 


                preBoundaryList = get_boundary_type("preboundarytypeId",2)

                primaryBoundaryList = get_boundary_type("primaryboundarytypeId",1)

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
                        rawQuerySet = \
                        Institution.objects.raw(""" SELECT "id","obj_id" FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = 1 """  % userId)
                        inst_list = [permObj.obj_id for permObj in
                                rawQuerySet]

                        # get the content objects(instituion, staff, student)
                        preSchListSql = """select id from schools_institution where id in %s and boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s))""" %(tuple(inst_list),2)
                        cursor.execute(preSchListSql)
                        res = cursor.fetchall()
                        preSchList = [i[0] for i in res]
                        primarySchListSql = """select id from schools_institution where id in %s and boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s))""" %(tuple(inst_list),1)
                        cursor.execute(primarySchListSql)
                        res = cursor.fetchall()
                        primarySchList = [i[0] for i in res]

                        preSchList = map(int, preSchList)
                        primarySchList = map(int, primarySchList)
                        if not preSchList:
                            preSchList=[0,0]
                        if not primarySchList:
                            primarySchList=[0,0]
                        for content in contentList:
                            (preList, primaryList) = ([00], [00])
                            contObj = \
                                ContentType.objects.get(app_label='schools'
                                    , name=content)
                            contId = contObj.id

                            if content == 'boundary':
                                (preBoundaryList,primaryBoundaryList) = ([], [])
                                # preschool boundary queries starts here
                                cursor.execute("select boundary_id from schools_institution where id in %s", [tuple(preSchList)])
                                res = cursor.fetchall()
                                BoundaryList = [i[0] for i in res]
                                preBoundaryList.extend(list(BoundaryList))

                                if not preBoundaryList:
                                    preBoundaryList=[0,0]
                                cursor.execute("select parent_id from schools_boundary where id in %s and boundary_type_id in ( select id from schools_boundary_type where id=%s)", [tuple(preBoundaryList),2])
                                res = cursor.fetchall()
                                BoundaryList = [i[0] for i in res]
                                preBoundaryList.extend(list(BoundaryList))

                                # preschool boundary queries ends here

                                # primary boundary list queries starts here
                                cursor.execute("select boundary_id from schools_institution where id in %s", [tuple(primarySchList)])
                                res = cursor.fetchall()
                                BoundaryList = [i[0] for i in res]
                                primaryBoundaryList.extend(list(BoundaryList))

                                if not primaryBoundaryList:
                                    primaryBoundaryList[0,0]
                                cursor.execute("select parent_id from schools_boundary where id in %s and boundary_type_id in ( select id from schools_boundary_type where id=%s)", [tuple(primaryBoundaryList),1])
                                res = cursor.fetchall()
                                BoundaryList = [i[0] for i in res]
                                primaryBoundaryList.extend(list(BoundaryList))

                                preList = preBoundaryList
                                primaryList = primaryBoundaryList

                            elif content == 'institution':
                                preList = preSchList
                                primaryList = primarySchList

                            elif content == 'staff':
                                cursor.execute("select id from schools_staff where institution_id in (select id from schools_institution where id in %s and boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s)))",[tuple(preSchList),2])
                                res = cursor.fetchall()
                                preStaffList = [i[0] for i in res]
                                if not preStaffList:
                                    preStaffList=[0,0]
                            
                                cursor.execute("select id from schools_staff where institution_id in (select id from schools_institution where id in %s and boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s)))",[tuple(primarySchList),1])
                                res = cursor.fetchall()
                                primaryStaffList = [i[0] for i in res]
                                if not primaryStaffList:
                                    primaryStaffList=[0,0]
                                preList = map(int, preStaffList)
                                primaryList = map(int,primaryStaffList)

                            elif content == 'student':
                                cursor.execute("select id from schools_studentgroup where institution_id in %s and institution_id in ( select id from schools_institution where boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s)))",[tuple(preSchList),2])
                                res = cursor.fetchall()
                                preSGList = [i[0] for i in res]
                                if not preSGList:
                                    preSGList=[0,0]

                                cursor.execute("select id from schools_studentgroup where institution_id in %s and institution_id in ( select id from schools_institution where boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s)))",[tuple(primarySchList),1])
                                res = cursor.fetchall()
                                primarySGList = [i[0] for i in res]
                                if not primarySGList:
                                    primarySGList=[0,0]

                                cursor.execute("select student_id from schools_Student_StudentGroupRelation where student_group_id in %s",[tuple(preSGList)])
                                res = cursor.fetchall()
                                preStList = [i[0] for i in res]

                                cursor.execute("select student_id from schools_Student_StudentGroupRelation where student_group_id in %s",[tuple(primarySGList)])
                                res = cursor.fetchall()
                                primaryStList = [i[0] for i in res]

                                if not preStList:
                                    preStList=[0,0]
                                if not primaryStList:
                                    primaryStList=[0,0]

                                preList = map(int, preStList)
                                primaryList = map(int,primaryStList)

                            #pre list fullhistory
                            cursor.execute("select count(id) from fullhistory_fullhistory where action_time>%s and action_time < %s and request_id in ( select id from fullhistory_request where user_pk = %s) and content_type_id in ( select id from django_content_type where id=%s) and CAST(object_id AS INT) in %s and action=%s",[sTime, eTime, userId, contId, tuple(preList),'C'])
                            res = cursor.fetchone()
                            dataList.append(int(res[0]))

                            cursor.execute("select count(id) as count from fullhistory_fullhistory where action_time > %s and action_time < %s and request_id in (select id from fullhistory_request where user_pk =%s ) and content_type_id in ( select id from django_content_type where id=%s) and CAST(object_id AS INT)  in %s and action=%s and data ~* %s",[sTime, eTime, userId, contId, tuple(preList),'U','active'])
                            res = cursor.fetchone()
                            dataList.append(int(res[0]))

                            cursor.execute("select count(id) as count from fullhistory_fullhistory where action_time > %s and action_time < %s and request_id in (select id from fullhistory_request where user_pk =%s ) and content_type_id in ( select id from django_content_type where id=%s) and CAST(object_id AS INT)  in %s and action=%s and not data  ~* %s ",[sTime, eTime, userId, contId, tuple(preList),'U','active'])
                            res = cursor.fetchone()
                            dataList.append(int(res[0]))


                            #primary list fullhistory
                            primaryList = map(int, primaryList)
                            cursor.execute("select count(id) from fullhistory_fullhistory where action_time>%s and action_time < %s and request_id in ( select id from fullhistory_request where user_pk = %s) and content_type_id in ( select id from django_content_type where id=%s) and CAST(object_id AS INT) in %s and action=%s",[sTime, eTime, userId, contId, tuple(primaryList),'C'])
                            res = cursor.fetchone()
                            dataList.append(int(res[0]))

                            cursor.execute("select count(id) as count from fullhistory_fullhistory where action_time > %s and action_time < %s and request_id in (select id from fullhistory_request where user_pk =%s ) and content_type_id in ( select id from django_content_type where id=%s) and CAST(object_id AS INT)  in %s and action=%s and data ~* %s ",[sTime, eTime, userId, contId, tuple(primaryList),'U','active'])
                            res = cursor.fetchone()
                            dataList.append(int(res[0]))

                            cursor.execute("select count(id) as count from fullhistory_fullhistory where action_time > %s and action_time < %s and request_id in (select id from fullhistory_request where user_pk =%s ) and content_type_id in ( select id from django_content_type where id=%s) and CAST(object_id AS INT)  in %s and action=%s and not data  ~* %s ",[sTime, eTime, userId, contId, tuple(primaryList),'U','active'])
                            res = cursor.fetchone()
                            dataList.append(int(res[0]))

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
                    print '%s.csv file has been created in %s/logFiles directory' % (fileName, cwd)
                    print 'Time taken: %s' %(datetime.datetime.now() - scriptStartTime)
            else:
                pass
            cursor.close()
        else:
            raise CommandError('Pass Startdate, end date and filename.\n')
