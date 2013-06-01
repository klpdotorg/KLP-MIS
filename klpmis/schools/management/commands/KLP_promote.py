#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from datetime import datetime
from django.db import connection
import pdb



class Command(BaseCommand):

    # args = '<inst_id inst_id ...>'
    # help = 'Students Promoting to Next Year'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        #pdb.set_trace()
        currentAcademic = Academic_Year.objects.get(name='2012-2013')  # current_academic

        currentYear = int(currentAcademic.name.split('-')[1])
        nextAcademic = str(currentYear) + '-' + str(currentYear + 1)
        currentAcademicObj = currentAcademic
        print 'CurrentAcademic Year :', current_academic().name
        print 'Next Academic Year  : ', nextAcademic
        nextAcademicObj = \
            Academic_Year.objects.get_or_create(name=nextAcademic)
        nextAcademicObj = (nextAcademicObj if not type(nextAcademicObj)
                           is tuple else nextAcademicObj[0])

        if args:
            institutions = Institution.objects.filter(id=args[0])
        else:
            institutions = \
                Institution.objects.filter(cat__category_type=1,
                    active=2)

        totalDic = {}
        totalpromotedStudDic = {}
        for inst in institutions:
            print 'Institution Name : ', inst.name, inst.id
            #pdb.set_trace()
            studentGroups = \
                StudentGroup.objects.filter(institution=inst,
                    active__in=[2,1], group_type='Class').order_by('name'
                    ).reverse()
            sgdic = studentGroups.values_list('id', 'name')
            sgidlist = {}
            sglist = []
            ressg = []
            for k in sgdic:
                try:
                    keyval = int(k[1])
                    sglist.append(keyval)
                except:
                    keyval = k[1]
                    ressg.append(keyval)
                if sgidlist.has_key(keyval):

                    val = sgidlist[keyval]
                    val.append(k[0])
                else:
                    val = [k[0]]

                sgidlist[keyval] = val

                # sglist=list(set([int(k[1]) for k in sgdic]))

            sglist = list(set(sglist))
            sglist.sort()
            sglist.reverse()
            totalsg = len(sglist) - 1
            sglist = sglist + ressg

                # print sglist,len(studentGroups),inst.id,sgdic,sgidlist
                # totalsg=len(sglist)
                # totalpromotedStudDic={}

            for sgid in sglist:
                totalpromotedStud = 0
                totalStud = 0
                if 1:
                    for k in sgidlist[sgid]:

                        sg = StudentGroup.objects.get(id=k)
                        print 'In student group [%s]: %s %s' % (sg.id,
                                sg.name, sg.section)
                        sg_stRealtions = \
                            Student_StudentGroupRelation.objects.filter(student_group=sg,
                                academic=currentAcademicObj, active__in=[1,2])  # .defer('child')
                        print 'Total Student in ', sg.name, sg.section, \
                            'is ', len(sg_stRealtions)

                        totalStud += len(sg_stRealtions)
                        if 1:  # sglist.index(sgid)!=0 or type(sgid) is not int or sgid<10 :
                            groupName = sg.name
                            try:
                                nxtGroup = int(groupName) + 1
                            except:
                                nxtGroup = groupName  # if Anganwadi class
                            groupSec = sg.section

                                # print "In student group [%s]: %s %s"%(sg.id, sg.name,sg.section)

                            if sg_stRealtions:
                                if type(sgid) is int:
                                    nextSg = \
    StudentGroup.objects.get_or_create(institution=inst, name=nxtGroup,
        section=groupSec, active__in=[0, 1, 2], group_type='Class')
                                    nextSg = \
    (nextSg if not type(nextSg) is tuple else nextSg[0])

                                    if nextSg.active != 2:
                                        nextSg.active = 2
                                        nextSg.save()
                                else:
                                    nextSg = sg

                                                    # nextSg.active=2
                                                    # nextSg.save()

                                print 'Next year student group [%s] activated' \
                                    % sg.id
                                srgquery =''
                                for sg_st in sg_stRealtions:
                                    studentObj = sg_st.student
                                    totalStud += 1

                                     # raw sql query for inserting bulk student
                                     # group relation 
                                     # starts here
                                    
                                    
                                    srgquery +=  ",(%s,%s,%s)"%(studentObj.id,nextSg.id,nextAcademicObj.id)
                                    totalpromotedStud += 1
                                    print 'Student %s promoted from %s %s to %s %s' \
    % (studentObj, sgid, sg.section, nextSg.name, nextSg.section)
                                if srgquery:
                                    try:
                                        cursor.execute("insert into schools_student_studentgrouprelation (student_id, student_group_id, academic_id, active) values"+ srgquery[1:])
                                    except:
                                        print "records already exists with this student id, student group id and academic id",srgquery[1:] 
                                    
                                    if 1:
                                        cursor.execute("insert into schools_student_studentgrouprelation_1(id, student_id, student_group_id, academic_id, active) select id, student_id, student_group_id, academic_id, 1 from schools_student_studentgrouprelation_2 where active=2 and academic_id=%s and student_group_id = %s" %(currentAcademicObj.id, nextSg.id))

                                        cursor.execute(" delete from schools_student_studentgrouprelation_2 where active=2 and academic_id=%s and student_group_id = %s" %(currentAcademicObj.id,nextSg.id))
                                    else:
                                        print "Intstitution id or academic id doesn't exist", nextSg.institution.id, currentAcademicObj.id
                                    # ends here
                            else:
                                totalpromotedStud += 0
                                sg_stRealtions.update(active=1)
                        else:

                            totalpromotedStud += len(sg_stRelations)
                            print 'ALL STUDENT  %s %s promoted  to OUT OF SCHOOL' \
                                % (sgid, sg.section)
                            sg_stRealtions.update(active=4)

                        # print 'Total Student in ',sg.name,sg.section ,'is ',totalStud

                    if totalDic.has_key(sg.name):
                        totalDic[sg.name] = totalDic[sg.name] \
                            + totalStud
                    else:
                        totalDic[sg.name] = totalStud
                    if totalpromotedStudDic.has_key(sg.name):
                        totalpromotedStudDic[sg.name] = \
                            totalpromotedStudDic[sg.name] \
                            + totalpromotedStud
                    else:
                        totalpromotedStudDic[sg.name] = \
                            totalpromotedStud
        print totalDic
        print totalpromotedStudDic


        self.stdout.write('Students Are Promoted ...\n')

            # prog=Programme.objects.filter(active=2) #end_date__range=[datetime.strptime(str(currentYear)+'-06-01','%Y-%m-%d'),datetime.strptime(str(currentYear+1)+'-05-31','%Y-%m-%d')])
            # assement=Assessment.objects.filter(programme__in=prog)
            # prog.update(active=1)

        self.stdout.write('Programmes are inActivated ...\n')


