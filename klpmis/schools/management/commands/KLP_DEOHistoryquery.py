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
from klpmis.settings import *
import pdb
from django.db import connection

def get_boundary_type(preboundarytypeId,btid):
    cursor = connection.cursor()
    preboundarytypeId = \
                    """select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=%d)""" % (btid)
    cursor.execute(preboundarytypeId)
    return [c[00] for c in cursor.fetchall()]

def institution_query(cid):
    cursor = connection.cursor()
    query = \
'SELECT distinct id from schools_institution where cat_id in (select id from schools_institution_category where category_type=%d)' % (cid)
    return query

def get_schoolIDs(preSchoolIds,fullhistoryQuery):
    slist = \
"""select distinct student_id  from schools_Student_StudentGroupRelation where student_group_id in (select id from schools_studentgroup where institution_id in  %s ) and student_id %s  """\
                                 % (preSchoolIds, fullhistoryQuery)
    return slist


def fhquery(qd):
    q = """select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s )  and CAST(object_id AS INT)  in %s and action='U' and (data like '%%anwsers%%' or data like '%%status%%' or data like '%%user2%%') and request_id  not in (select id from fullhistory_request where user_pk =%s )""" \
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
        contentList = ['institution', 'student', 'staff']
        
        d = DATABASES['default']
        datebase = d['NAME']
        user = d['USER']
        password = d['PASSWORD']
        connection = psycopg2.connect(database=datebase, user=user,
                password=password)

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

                headerList = [
                    'Sl.No',
                    'User',
                    'pre_sch_created',
                    'pre_sch_mod',
                    'pre_sch_del',
                    'primary_sch_created',
                    'primary_sch_mod',
                    'primary_sch_del',
                    'pre_stud_created',
                    'pre_stud_mod',
                    'pre_stud_del',
                    'primary_stud_created',
                    'primary_stud_mod',
                    'primary_stud_del',
                    'pre_teacher_created',
                    'pre_teacher_mod',
                    'pre_teacher_del',
                    'primary_teacher_created',
                    'primary_teacher_mod',
                    'primary_teacher_del',
                    ]
                (asmDict, asmList) = ({}, [])
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
                
                assessments = Assessment.objects.all().values_list('id', flat = True)
                cursor = connection.cursor()
                fullhistoryAnswers = \
                    cursor.execute("""select distinct CAST(object_id AS INT) from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and content_type_id in ( select id from django_content_type where name='answer')"""
                                    % (sTime, eTime))
                validAns = [c[00] for c in cursor.fetchall()]

                preBoundaryList = get_boundary_type("preboundarytypeId",2)

                primaryBoundaryList = get_boundary_type("primaryboundarytypeId",1)
                user_ids = tuple(userIds)

                for assessment in assessments:
                    questions = \
                        """select id from schools_question where assessment_id= %s and active= 2"""\
                         % assessment
                    answerQuery = \
                        """ select distinct id from schools_answer  where (user1_id in %s or  user2_id in %s  ) and  question_id in (%s)  and id in %s"""\
                         % (user_ids, user_ids, questions,
                            tuple(validAns))
                    cursor.execute(answerQuery)
                    answersCur = cursor.fetchall()  # Answer.objects.raw(answerQuery)
                    answers = [c[00] for c in answersCur]
                    if 1:
                        if len(list(answers)):
                            print assessment
                            assessmentId = assessment
                            headerList.append('Assess Id')
                            progname = Assessment.objects.get(id=assessmentId)
                            asmName = '%s-%s'\
                                 % (progname.programme.name,
                                    progname.name)
                            headerList.append(asmName
                                     + ' Num Of correct Entries')
                            headerList.append(asmName
                                     + ' Num Of incorrect Entries')
                            headerList.append(asmName
                                     + ' Num Of verified Entries')
                            headerList.append(asmName
                                     + ' Num Of rectified Entries')

                            asmDict[assessmentId] = answers  # answerQuery
                print 'header built'
                historyFile.writerow(headerList)
                count = 0
                users = User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'],is_active=1).order_by('username')
                for user in users:
                    
                    count += 1
                    userId = user.id
                    dataList = [count, user.username]

                    preinstitutionQuery = institution_query(2)
                    cursor.execute(preinstitutionQuery)
                    preSchoolIds = tuple([c[00] for c in
                                    cursor.fetchall()])
                    primaryinstitutionQuery = institution_query(1)
                    cursor.execute(primaryinstitutionQuery)
                    schoolIds = tuple([c[00] for c in
                    cursor.fetchall()])
                                    
                    for content in contentdic:
                        contId = contentdic[content]
                        fullhistoryQuery = \
                            """ in (select CAST(object_id AS INT) from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and content_type_id =%s )"""\
                             % (sTime, eTime, userId, contId)


                        if content == 'institution':
                            preList = """%s and id %s """\
                                 % (preinstitutionQuery,
                                    fullhistoryQuery)
                            cursor.execute(preList)

                            preListId = tuple([c[00] for c in
                                    cursor.fetchall()])

                            primaryList = """%s and id %s """\
                                 % (primaryinstitutionQuery,
                                    fullhistoryQuery)
                            primaryListId = tuple([c[00] for c in
                                    cursor.fetchall()])
                        elif content == 'staff':

                            preList = \
                                """select distinct id from schools_staff where institution_id in %s and id %s """\
                                 % (preSchoolIds, fullhistoryQuery)

                            primaryList = \
                                """select distinct id from schools_staff where institution_id in %s and id %s """\
                                 % (schoolIds, fullhistoryQuery)
                        elif content == 'student':
                            if preSchoolIds:
                                preList = get_schoolIDs(preSchoolIds,fullhistoryQuery)
                            else:
                                preList=[]

                            if schoolIds:
                                primaryList = get_schoolIDs(schoolIds,fullhistoryQuery)
                            else:
                                primaryList=[]

                        if content == 'institution':
                            loopList = [preListId, primaryListId]
                        else:
                            loopList = [preList, primaryList]
                        for listobj in loopList:

                            if content in ['institution', 'staff',
                                    'studentgroup', 'student']:
                                createdhistoryraw = \
                                    """select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and content_type_id =%s  and action='C' """\
                                     % (sTime, eTime, userId, contId)
                                updatedhistoryraw = \
                                    """select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and content_type_id =%s and action='U'"""\
                                     % (sTime, eTime, userId, contId)

                                if listobj:
                                    createdhistoryraw += \
    'and CAST(object_id AS INT) in (%s)' % listobj
                                    updatedhistoryraw += \
    'and CAST(object_id AS INT) in (%s)' % listobj

                                activeupdated = updatedhistoryraw\
                                     + """ and data ilike '%%active%%'"""
                                notactiveupdated = updatedhistoryraw\
                                     + """ and data not ilike '%%active%%'"""

                                cursor.execute(createdhistoryraw)
                                row = cursor.fetchone()
                                dataList.append(row and row[00] or 00)

                                cursor.execute(notactiveupdated)
                                row = cursor.fetchone()
                                dataList.append(row and row[00] or 00)

                                cursor.execute(activeupdated)
                                row = cursor.fetchone()
                                dataList.append(row and row[00] or 00)
                            else:

                                dataList = dataList + [00, 00, 00]

                    (loopList, preList, primaryList) = ([], [], [])
                    print 'userId being processed: ', userId
                    for asmId in asmDict:
                        answers = tuple([i for i in asmDict[asmId]])
                        if len(answers) == 1:
                            answers = str(answers).replace(",",'')
                        
                        if 1:
                            crQuery = \
                                """select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s )  and CAST(object_id AS INT)  in %s and action='C'"""\
                                 % (sTime, eTime, userId, answers)

                            cursor.execute(crQuery)
                            row = cursor.fetchone()
                            crEntriesData = row and row[00] or 00
                            crEntries = crEntriesData

                            if crEntries == 00:
                                inCrEntries = 00
                            else:
                                qd = {'sTime':sTime,'eTime':eTime,'userId':userId,'answers':answers,'userId':userId}
                                inCrQuery = fhquery(qd)
                                

                                cursor.execute(inCrQuery)
                                row = cursor.fetchone()
                                inCrEntries = row and row[00] or 00

                                crEntries = crEntries - inCrEntries
                            rd = {'sTime':sTime,'eTime':eTime,'userId':userId,'answers':answers,'userId':userId}
                            vQuery = fhrquery(rd)

                            cursor.execute(vQuery)
                            row = cursor.fetchone()
                            vEntries = row and row[00] or 00  # len(list(FullHistory.objects.raw(vQuery)))
    
                            rQuery = \
                                """select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and CAST(object_id AS INT)  in %s and action='U' and (data like '%%anwsers%%' or data like '%%status%%' or data like '%%user2%%') and request_id  not in (select id from fullhistory_request where user_pk =%s )  and (data not like '%%id%%' or data not like '%%question%%' or data not like '%%student%%')"""\
                                 % (sTime, eTime, userId, answers,
                                    userId)

                            cursor.execute(rQuery)
                            row = cursor.fetchone()
                            rEntries = row and row[00] or 00  # #len(list(FullHistory.objects.raw(rQuery)))

                            vEntries = vEntries - rEntries

                            dataList.append(asmId)
                            dataList.append(crEntries)
                            dataList.append(inCrEntries)
                            dataList.append(vEntries)
                            dataList.append(rEntries)

                    historyFile = csv.writer(open(genFile, 'a'))
                    historyFile.writerow(dataList)

                print '%s.csv file has been created in %s/logFiles directory'\
                     % (fileName, cwd)
                print 'Time taken: %s' %(datetime.datetime.now() - scriptStartTime)
            else:
                pass

            cursor.close()
        else:

            raise CommandError('Pass Startdate, end date and filename.\n'
                               )


