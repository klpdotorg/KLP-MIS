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

def data_appendList(listname):
    
    dataList.append(FullHistory.objects.filter(action_time__range=(sTime,
                                        eTime),
                                        request__user_pk=userId,
                                        content_type__id=contId,
                                        object_id__in=listname,
                                        action='C').count())
    dataList.append(FullHistory.objects.filter(action_time__range=(sTime,
                                        eTime),
                                        request__user_pk=userId,
                                        content_type__id=contId,
                                        object_id__in=listname,
                                        action='U'
                                        ).exclude(_data__icontains='active'
                                        ).count())

    dataList.append(FullHistory.objects.filter(
                                    action_time__range=(sTime, eTime),
                                    request__user_pk=userId,
                                    content_type__id=contId,
                                    object_id__in=listname,
                                    action='U',
                                    _data__icontains='active',
                                    ).count())
    return True


def boundary_list_query(listname,btype,fieldtype):
    return Boundary.objects.filter(id__in=listname,
                            boundary_type__id=btype).values_list(fieldtype,
        flat=True).distinct()

def institution_list_query(listname,fieldtype):
    return Institution.objects.filter(id__in=listname,
                            boundary_type__id=2).values_list(fieldtype,
        flat=True).distinct()

class Command(BaseCommand):

    ''' Command To generate Data Entry Operators History in csv format.'''

    def handle(self, *args, **options):
        if 1:

                    # read start date, end date and filename

            start_date = args[00]
            end_date = args[1]
            fileName = args[2]
            contentList = ['boundary', 'institution', 'student', 'staff'
                           ]
            if fileName and start_date and end_date:
                try:
                    strDate = start_date.split('/')
                    enDate = end_date.split('/')
                    assessments = \
                        Assessment.objects.select_related('programme'
                            ).filter(programme__active=2,
                            active=2).distinct().only('id', 'name')

                        # get current working directory.

                    cwd = os.getcwd()
                    path = '%s/logFiles/' % cwd
                    if not os.path.exists(path):

                                            # if dir not exists creates directory with name logfiles in cwd.

                        os.makedirs(path)

                                        # create csv file with the name passed.

                    genFile = '%s/%s.csv' % (path, fileName)
                    historyFile2 = csv.writer(open(genFile, 'wb'))

                    # Write header

                    headerList = [
                        'Sl.No',
                        'User',
                        'pre_boundary_created',
                        'pre_boundary_mod',
                        'pre_boundary_del',
                        'primary_boundary_created',
                        'primary_boundary_mod',
                        'primary_boundary_del',
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
                    users = User.objects.filter(is_active=1)  # .filter(username__iexact="nalini").order_by("username").only("id", "username")
                    userIds = users.values_list('id', flat=True)
                    sDate = datetime.date(int(strDate[2]),
                            int(strDate[1]), int(strDate[00]))
                    eDate = datetime.date(int(enDate[2]),
                            int(enDate[1]), int(enDate[00]))
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
                    print sTime, eTime
                    for assessment in assessments:

                        answers = \
                            Answer.objects.filter(Q(user1__id__in=userIds)
                                | Q(user2__id__in=userIds),
                                last_modified_date__range=(sDate, eDate),
                                question__assessment=assessment).values_list('id'
                                , flat=True).distinct()
                        if answers:
                            assessmentId = assessment.id
                            asmList.append(assessmentId)
                            asmName = '%s-%s' \
                                % (assessment.programme.name,
                                   assessment.name)
                            headerList.append(asmName
                                    + ' Num Of correct Entries')
                            headerList.append(asmName
                                    + ' Num Of incorrect Entries')
                            headerList.append(asmName
                                    + ' Num Of verified Entries')
                            headerList.append(asmName
                                    + ' Num Of rectified Entries')
                            nList = [i for i in answers]
                            nList.append(00)
                            asmDict[assessmentId] = nList
                    historyFile2.writerow(headerList)

                                        # historyFile2.close()

                    count = 00

                    # print User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'], is_active=1).order_by("username").values_list('id',flat=True)....................

                    for user in \
                        User.objects.filter(groups__name__in=['Data Entry Executive'
                            , 'Data Entry Operator'],
                            is_active=1).order_by('username'):
                        if user.id:
                            print count, \
                                '********************************************', \
                                user.id
                            count += 1
                            userId = user.id

                            dataList = [count, user.username]

                            rawQuerySet = \
                                Institution.objects.raw(""" SELECT "id","obj_id" FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = 1 """
                                     % userId)
                            inst_list = [permObj.obj_id for permObj in
                                    rawQuerySet]

                        # get the content objects(instituion, staff, student)

                            preSchList = \
                                Institution.objects.filter(id__in=inst_list,
                                    boundary__boundary_type__id=2).values_list('id'
                                    , flat=True)
                            primarySchList = \
                                Institution.objects.filter(id__in=inst_list,
                                    boundary__boundary_type__id=1).values_list('id'
                                    , flat=True)

                            preSchList = map(int, preSchList)
                            primarySchList = map(int, primarySchList)
                            for content in contentList:

                                                        # print content

                                (preList, primaryList) = ([00], [00])
                                contObj = \
                                    ContentType.objects.get(app_label='schools'
                                        , name=content)
                                contId = contObj.id
                                if content == 'boundary':
                                    (preBoundaryList,
        primaryBoundaryList) = ([], [])
                                    BoundaryList = institution_list_query(preSchList,'boundary')
                                    preBoundaryList.extend(list(BoundaryList))

                                    # print preBoundaryList,'LLLLLLLLLLLLLLLLLLLLLLLl'
                                    BoundaryList = boundary_list_query(preBoundaryList,2,'parent')
                                    preBoundaryList.extend(list(BoundaryList))


                                    BoundaryList = boundary_list_query(preBoundaryList,1,'parent')
                                    preBoundaryList.extend(list(BoundaryList))


                                    BoundaryList = institution_list_query(primarySchList,'boundary')
                                    primaryBoundaryList.extend(list(BoundaryList))

                                    BoundaryList = boundary_list_query(primaryBoundaryList,1,'parent')
                                    primaryBoundaryList.extend(list(BoundaryList))

                                    BoundaryList = boundary_list_query(primaryBoundaryList,2,'parent')
                                    primaryBoundaryList.extend(list(BoundaryList))

                                    preList = preBoundaryList  # ['%s' %i for i in preBoundaryList]
                                    primaryList = primaryBoundaryList  # ['%s' %i for i in primaryBoundaryList]
                                elif content == 'institution':

                                                                # print primaryList[:5]

                                    preList = preSchList  # ['%s' %i for i in preSchList]
                                    primaryList = primarySchList  # ['%s' %i for i in primarySchList]
                                elif content == 'staff':
                                    preStaffList = \
    Staff.objects.filter(institution__id__in=preSchList,
                         institution__boundary__boundary_type__id=2).values_list('id'
        , flat=True)
                                    primaryStaffList = \
    Staff.objects.filter(institution__id__in=primarySchList,
                         institution__boundary__boundary_type__id=1).values_list('id'
        , flat=True)
                                    preList = map(int, preStaffList)  # ['%s' %i for i in preStaffList]
                                    primaryList = map(int,
        primaryStaffList)  # ['%s' %i for i in primaryStaffList]
                                elif content == 'student':

                                                                # print primaryList[:5]

                                    preSGList = \
    StudentGroup.objects.filter(institution__id__in=preSchList,
                                institution__boundary__boundary_type__id=2).values_list('id'
        , flat=True)

                                    primarySGList = \
    StudentGroup.objects.filter(institution__id__in=primarySchList,
                                institution__boundary__boundary_type__id=1).values_list('id'
        , flat=True)

                                    preStList = \
    Student_StudentGroupRelation.objects.filter(student_group__id__in=preSGList).values_list('student'
        , flat=True)

                                    primaryStList = \
    Student_StudentGroupRelation.objects.filter(student_group__id__in=primarySGList).values_list('student'
        , flat=True)

                                    preList = map(int, preStList)
                                    data_appendList(preList)
                                
                                    primaryList = map(int, primaryList)
                                    data_appendList(primaryList)
                                

                                                        # print '13'
                                    # print dataList....
                                # dataList.extend([0, 0, 0, 0, 0, 0])

                            for asmId in asmList:
                                answers = asmDict[asmId]

                                                        # print answers,sTime,eTime

                                if answers:

                                                                # print 'ans',answers[:5],asmId
                                    # answers=[int(k) for k in answers]....

                                    crEntriesData = \
    FullHistory.objects.filter(action_time__range=(sTime, eTime),
                               request__user_pk=userId,
                               object_id__in=answers, action='C')
                                    crEntries = crEntriesData.count()

                                                                # print 'crEntris'

                                    if crEntries == 00:
                                        inCrEntries = 00
                                    else:
                                        crEntriesLis = \
    list(crEntriesData.values_list('object_id', flat=True))

                                                                        # crEntriesLis=[int(k) for k in crEntriesLis ]

                                        inCrEntries = \
    FullHistory.objects.filter((Q(_data__icontains='answer')
                               | Q(_data__icontains='status'))
                               & Q(_data__icontains='user2'),
                               action_time__range=(sTime, eTime),
                               object_id__in=crEntriesLis, action='U'
                               ).exclude(request__user_pk=userId).count()

                                        crEntries = crEntries \
    - inCrEntries

                                    vEntries = \
    FullHistory.objects.filter(action_time__range=(sTime, eTime),
                               request__user_pk=userId,
                               object_id__in=answers, action='U',
                               _data__icontains='user2'
                               ).exclude(Q(_data__icontains='id')
        | Q(_data__icontains='question') | Q(_data__icontains='student'
        )).count()

                                    rEntries = \
    FullHistory.objects.filter((Q(_data__icontains='answer')
                               | Q(_data__icontains='status'))
                               & Q(_data__icontains='user2'),
                               action_time__range=(sTime, eTime),
                               request__user_pk=userId,
                               object_id__in=answers, action='U'
                               ).exclude(Q(_data__icontains='id')
        | Q(_data__icontains='question') | Q(_data__icontains='student'
        )).count()

                                    vEntries = vEntries - rEntries

                                    # print userId,crEntries,inCrEntries,vEntries,rEntries

                                    dataList.append(crEntries)
                                    dataList.append(inCrEntries)
                                    dataList.append(vEntries)
                                    dataList.append(rEntries)

                            # Written data into file.

                            print dataList
                            historyFile2 = csv.writer(open(genFile, 'a'
                                    ))
                            historyFile2.writerow(dataList)

                    # historyFile1.close()....

                    print '%s.csv file has been created in %s/logFiles directory' \
                        % (fileName, cwd)
                except IndexError:

                                    # if arguments are not proper raises an command error.

                    raise CommandError('Date Should be in dd/mm/yyyy format.\n'
                            )
                except ValueError:

                    # if arguments are not proper raises an command error.

                    raise CommandError('Date Should be in dd/mm/yyyy format.\n'
                            )
            else:

                            # if arguments are not passed raises an command error.

                raise CommandError('Pass Startdate, end date and filename.\n'
                                   )
        else:

                      # xcept IndexError:
                    # if arguments are not passed raises an command error.

            raise CommandError('Pass Startdate, end date and filename.\n'
                               )


