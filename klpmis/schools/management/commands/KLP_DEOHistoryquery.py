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
                # get all active assessments
                assessments = Assessment.objects.filter(active=2).distinct().only("id", "name")
                cursor = connection.cursor()

                # get answers which are in fullhistory
                fullhistoryAnswers = \
                    cursor.execute("""select distinct CAST(object_id AS INT) from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and content_type_id in ( select id from django_content_type where name='%s')"""
                                    % (sTime, eTime,'answer'))
                validAns = "0 "
                for c in cursor.fetchall():
                    validAns += ", %s"%c[00] 


                preBoundaryList = get_boundary_type("preboundarytypeId",2)

                primaryBoundaryList = get_boundary_type("primaryboundarytypeId",1)

                user_ids = tuple(userIds)

                # iteatate on each assessment
                for assessment in assessments:
                    # get active questions for each assessment
                    questions = \
                        """select id from schools_question where assessment_id= %s and active= 2"""\
                         % assessment.id
                    cursor.execute(questions)
                    resq = cursor.fetchall()
                    qlist = "0 "

                    for i in resq:
                        qlist += ", %s "%(i[0])
                    # get answers for each assessment
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
                #get all active DEE, DEO's
                users = User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'], is_active=1).order_by("username")
                if users:
                    for user in users:
                        count += 1
                        userId = user.id
                        dataList = [count, user.username]
                        # get institutions for each user id
                        rawQuerySet = \
                        Institution.objects.raw(""" SELECT "id","obj_id" FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = 1 """  % userId)
                        inst_list = [permObj.obj_id for permObj in
                                rawQuerySet]

                        # get the content objects(instituion, staff, student)
                        # get the preschool list
                        preSchListSql = """select id from schools_institution where id in %s and boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s))""" %(tuple(inst_list),2)
                        cursor.execute(preSchListSql)
                        res = cursor.fetchall()
                        preSchList = [i[0] for i in res]

                        # get the primary school list
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
                        # iteatate over each contentList
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
                                # primary boundary list queries ends here

                            elif content == 'institution':
                                # institution queries starts here
                                preList = preSchList
                                primaryList = primarySchList
                                # institution queries ends here

                            elif content == 'staff':
                                # staff queries starts here
                                # preschool staff list
                                cursor.execute("select id from schools_staff where institution_id in (select id from schools_institution where id in %s and boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s)))",[tuple(preSchList),2])
                                res = cursor.fetchall()
                                preStaffList = [i[0] for i in res]
                                if not preStaffList:
                                    preStaffList=[0,0]
                                # primary school staff list
                                cursor.execute("select id from schools_staff where institution_id in (select id from schools_institution where id in %s and boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s)))",[tuple(primarySchList),1])
                                res = cursor.fetchall()
                                primaryStaffList = [i[0] for i in res]
                                if not primaryStaffList:
                                    primaryStaffList=[0,0]
                                preList = map(int, preStaffList)
                                primaryList = map(int,primaryStaffList)
                                # staff queries ends here

                            elif content == 'student':
                                # student queries starts here
                                # preschool students group query
                                cursor.execute("select id from schools_studentgroup where institution_id in %s and institution_id in ( select id from schools_institution where boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s)))",[tuple(preSchList),2])
                                res = cursor.fetchall()
                                preSGList = [i[0] for i in res]
                                if not preSGList:
                                    preSGList=[0,0]

                                #primary school students group query
                                cursor.execute("select id from schools_studentgroup where institution_id in %s and institution_id in ( select id from schools_institution where boundary_id in (select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%s)))",[tuple(primarySchList),1])
                                res = cursor.fetchall()
                                primarySGList = [i[0] for i in res]
                                if not primarySGList:
                                    primarySGList=[0,0]
                                # get preschool students
                                cursor.execute("select student_id from schools_Student_StudentGroupRelation where student_group_id in %s",[tuple(preSGList)])
                                res = cursor.fetchall()
                                preStList = [i[0] for i in res]

                                # get primary school students
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
                            if answers:
                                #correct entires sql
                                crQuery = """select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s )  and CAST(object_id AS INT)  in %s and action='C'""" % (sTime, eTime, userId, tuple(answers))
                                cursor.execute(crQuery)
                                res = cursor.fetchone()
                                crEntries = int(res[0])
                                if crEntries == 00:
                                    inCrEntries = 00
                                else:
                                    # objecct id's for incorrect entries sql
                                    crQueryData = """select object_id as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s )  and CAST(object_id AS INT)  in %s and action='C'""" % (sTime, eTime, userId, tuple(answers))
                                    cursor.execute(crQueryData)
                                    res = cursor.fetchall()
                                    crEntriesLis = [i[0] for i in res]
                                    if not crEntriesLis:
                                        crEntriesLis = [0,0]
                                    # incorrect entries sql
                                    cursor.execute("select count(id) from fullhistory_fullhistory where request_id not in ( select id from fullhistory_request where user_pk=%s) and action_time > %s and action_time < %s and CAST(object_id AS INT) in %s and (data ~* %s or data ~* %s) and data ~* %s ",[userId, sTime, eTime, tuple(crEntriesLis),'answer','status','user2'])
                                    res = cursor.fetchone()
                                    inCrEntries = int(res[0])
                                    crEntries = crEntries - inCrEntries

                                # verified entries sql
                                cursor.execute("select count(id) from fullhistory_fullhistory where (request_id in ( select id from fullhistory_request where user_pk=%s) and action_time > %s and action_time < %s and CAST(object_id AS INT) in %s and action = 'U' and data ~* %s and not (data ~* %s or data ~* %s or data ~* %s)) ",[userId,sTime,
eTime,tuple(answers),'user2','id','question','student'])
                                res = cursor.fetchone()
                                vEntries = int(res[0])

                                # rectfied entires sql
                                cursor.execute("select count(id) from fullhistory_fullhistory where action_time > %s and action_time < %s and CAST(object_id AS INT) in %s and request_id in ( select id from fullhistory_request where user_pk=%s and (data ~* %s or data ~* %s ) and data ~* %s ) and action = 'U' and not (data ~* %s or data ~* %s or data ~* %s)" ,[sTime,eTime, tuple(answers),userId,'answer','status','user2','id','question','student'])
                                res = cursor.fetchone()
                                rEntries = int(res[0])

                                vEntries = vEntries - rEntries
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
