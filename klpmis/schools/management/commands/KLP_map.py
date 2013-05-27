#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from schools.models import *
import django
import datetime
import os
import csv
import pdb
from klprestApi.TreeMenu import KLP_assignedInstitutions
import datetime
from django.db import transaction

from schools.forms import *
from django.forms.models import modelformset_factory

def cmpT(t1, t2): 
    return sorted(t1) == sorted(t2)

class Command(BaseCommand):

    ''' Command To map assessments with student group and to assign permissions to users automatically. And then it list out the user permissions.'''

    @transaction.autocommit
    def handle(self, *args, **options):
        if 1:
           
            # Reads the arguments from command line.

            fileName = args[0]
            assessment_id = args[1]
            try:
                reportflag = args[2]
            except:
                reportflag = 0

            # checks for arguments
            #pdb.set_trace()
            starttime = procestime = datetime.datetime.now()
            self.stdout.write('The mapping is started at %s\n'
                              % starttime)
            asstypedic = {1: 'Institution', 2: 'Student',
                          2: 'Student Group'}
            if fileName and assessment_id:
                if 1: 
                    mapFile = open(fileName, 'r')  # open file to read data
                    studenGroups = mapFile.read().replace('\n', '')  # read data from file
                    mapFile.close()  # Close file after reading data
                    sgList = studenGroups.split(',')  #  splits student group ids by ,
                    assessmentObj = \
                        Assessment.objects.filter(id=assessment_id).defer('programme'
                            )[0]  # get assessment object.

                    # get assessment list under programme to assign permissions to user.

                    prgObj = assessmentObj.programme
                    Asstype = assessmentObj.typ

                    assessment_list = \
                        Assessment.objects.filter(programme=prgObj,
                            active=2).defer('programme'
                            ).values_list('id', flat=True).distinct()
                    inst_list = []
                      
                    for sg in sgList:

                        if sg:
                            if assessmentObj.typ in [2, 3]:
                                errormsg = \
                                    '%s student Group id does not exist ' \
                                    % sg
                                sgObj = \
                                    StudentGroup.objects.filter(id=int(sg)).defer('institution'
                                        )
                                if sgObj:
                                    sgObj = sgObj[0]  # get student group object
                                    inst_list.append(sgObj.institution.id)
                            else:
                                errormsg = \
                                    '%s Institution id does not exist ' \
                                    % sg
                                sgObj = \
                                    Institution.objects.filter(id=int(sg)).defer('boundary'
                                        , 'cat', 'mgmt', 'inst_address')
                                if sgObj:
                                    sgObj = sgObj[0]
                                    inst_list.append(int(sg))
                            if sgObj:
                                AssStudAssForm= modelformset_factory(Assessment_StudentGroup_Association,form=Assessment_StudentGroup_Association_Form)

                                requestcopy={} #request #.POST.copy()
                                requestcopy['form-0-student_group']=sgObj.id
                                requestcopy['form-0-active']=2
                                requestcopy['form-0-assessment']=assessmentObj.id
                                requestcopy['form-TOTAL_FORMS']=1
                                requestcopy['form-MAX_NUM_FORMS']=1000

                                if assessmentObj.typ == 3:

                                                     # mapping assesment and student group
                                    ASAObj=Assessment_StudentGroup_Association.objects.filter(student_group=sgObj,  assessment=assessmentObj)
                                    #mapObj = \Assessment_StudentGroup_Association(assessment=assessmentObj,student_group=sgObj, active=2)
                                    AssStudAssForm= modelformset_factory(Assessment_StudentGroup_Association,form=Assessment_StudentGroup_Association_Form)
                                    MappingStr = \
    '%s - Assessment and StudentGroup - %s%s ...\n' \
    % (assessmentObj.name, sgObj.name, sgObj.section)
                                elif assessmentObj.typ == 2:

                                                                # mapping assesment and student group
                                    ASAObj=Assessment_Class_Association.objects.filter(student_group=sgObj,  assessment=assessmentObj)
                                    #mapObj = \Assessment_Class_Association(assessment=assessmentObj,student_group=sgObj, active=2)
                                    AssStudAssForm= modelformset_factory(Assessment_Class_Association,form=Assessment_Class_Association_Form)
                                    MappingStr = \
    '%s - Assessment and StudentGroup - %s%s ...\n' \
    % (assessmentObj.name, sgObj.name, sgObj.section)
                                else:

                                                                # mapping assement and Institution
                                    ASAObj=Assessment_Institution_Association.objects.filter(institution=sgObj,  assessment=assessmentObj) 
                                    # mapObj = \Assessment_Institution_Association(assessment=assessmentObj,institution=sgObj, active=2)
                                    AssStudAssForm= modelformset_factory(Assessment_Institution_Association,form=Assessment_Institution_Association_Form)
                                    MappingStr = \
    '%s - Assessment and Institution %s ...\n' % (assessmentObj.name,
        sgObj.name)
                                   
                                if ASAObj:
                                        '''requestcopy['form-INITIAL_FORMS']=1
                                        requestcopy['form-0-id']=ASAObj[0].id        
                                        rform = AssStudAssForm(requestcopy,requestcopy,queryset=ASAObj)
                                        '''
                                        self.stdout.write('%s are Already Mapped ...\n'   % MappingStr)
                                else:
                                          requestcopy['form-INITIAL_FORMS']=0
                                          rform = AssStudAssForm(requestcopy,requestcopy) 
                                                        
                                          if rform.errors[0].has_key('__all__'):
                                                     self.stdout.write('%s are Already Mapped ...\n'
         % MappingStr)
                                          else:
                                             try:
                                                 ascopy = Assessment_Institution_Association.objects.get(institution__id=requestcopy['form-0-student_group']
                                             ,assessment__id = requestcopy['form-0-assessment'])
                                             except:
                                                 if not assessmentObj.typ == 1:
                                                    rform.save()
                                                 else:
                                                     if not Assessment_Institution_Association.objects.filter(assessment__id=requestcopy['form-0-assessment'], institution__id = requestcopy['form-0-assessment']).exists():
                                                         from django.db import connection
                                                         cursor = connection.cursor()
                                                         q1 = """select count(*) from schools_assessment_institution_association where assessment_id = %d and institution_id = %d and active=2 """ %(requestcopy['form-0-assessment'],requestcopy['form-0-student_group'])
                                                         cursor.execute(q1)
                                                         res = cursor.fetchone()
                                                         bt = (0L,)
                                                         qres = cmpT(res,bt)
                                                         if qres:
                                                             qu = """insert into schools_Assessment_Institution_Association(assessment_id, institution_id, active) \
                                                             values (%s, %s, 2) """ %(requestcopy['form-0-assessment'],requestcopy['form-0-student_group'])
                                                             cursor.execute(qu)
                                                         else:
                                                             print "record exist"
                                                 self.stdout.write('%s are Mapped ...\n'
         % MappingStr)
                                '''
                                try:
                                    mapObj.save()
                                    self.stdout.write('%s are Mapped ...\n'
         % MappingStr)
                                except django.db.utils.IntegrityError:
                                    django.db.connection._rollback()
                                    self.stdout.write('%s are Already Mapped ...\n'
         % MappingStr) 
                                '''
                            else:
                                self.stdout.write('\n %s ' % errormsg)

                    # get users to assign permissions........

                    users_List = \
                        User.objects.filter(groups__name__in=['Data Entry Executive'
                            , 'Data Entry Operator'],
                            is_active=1).defer('groups')
                    inst_list = list(set(inst_list))
                    if reportflag:
                        cwd = os.getcwd()
                        path = '%s/logFiles/' % cwd
                        if not os.path.exists(path):
                            os.makedirs(path)
                        instPermCsv = '%s/%s.csv' % (path,
                                'instpermissions')
                        instPermFile = csv.writer(open(instPermCsv, 'wb'
                                ))
                        asmPermCsv = '%s/%s.csv' % (path,
                                'assessmentPermissions')
                        asmPermFile = csv.writer(open(asmPermCsv, 'wb'))
                        instPermFile.writerow(['User', 'Institutions',
                                'Boundaries'])
                        asmPermFile.writerow(['User', 'Institutions',
                                'Boundaries', 'Assessment', 'Programme'
                                ])
                    self.stdout.write('Total No of User %s \n'
                            % len(users_List))
                    userNo = 1
                    self.stdout.write('Total No Of Institution for Assessment %s \n '
                             % len(inst_list))
                    for user in users_List:

                                                # get institutions assigned to user to generate report and to verify user permission.

                        self.stdout.write('\n%s .Now performing %s ,'
                                % (str(userNo), user.username))
                        print user.username
                        #pdb.set_trace()
                        perm_instList = \
                            KLP_assignedInstitutions(user.id)
                        perm_instSet = \
                            list(set(inst_list).intersection(set(perm_instList)))
                        InsObjs = \
                            Institution.objects.filter(id__in=perm_instSet).defer('boundary'
                                , 'cat', 'mgmt', 'inst_address')
                        TotalInst = InsObjs.values_list('id',
                                flat=True).distinct()
                        self.stdout.write(' Total Institution %s is assigned to %s'
                                 % (len(TotalInst), user.username))
                        asmPerm = []

                        userNo += 1

                        # get user permissions in progr

                        permObjs = \
                            UserAssessmentPermissions.objects.filter(user=user,
                                assessment__id__in=assessment_list,
                                access=1).defer('user', 'assessment')
                        if len(permObjs) >= 1:
                            asmPerm.append(True)
                        lenTrue = asmPerm.count(True)
                        lenAsm = len(assessment_list)
                        inscount = 0
                        for instObj in InsObjs:

                                # if users has permission for all assessments in programme
                                # check user has permission with instituion.
                                                                # if user has permission then assign assessment permission

                            if reportflag:
                                permInstObj = instObj

                                                                # To generate Institution permission report

                                instPermData = []
                                boundaryStr = '%s --> %s --> %s' \
                                    % (permInstObj.boundary,
                                        permInstObj.boundary.parent,
                                        permInstObj.boundary.parent.parent)
                                if inscount == 0:
                                    instPermData.append(user)
                                else:
                                    instPermData.append(' ')
                                inscount = 1
                                instPermData.append(permInstObj.name)
                                instPermData.append(boundaryStr)
                                instPermFile.writerow(instPermData)

                            if lenTrue == lenAsm or lenTrue == lenAsm \
                                - 1:
                                 UserPermForm= modelformset_factory(UserAssessmentPermissions,form=UserAssessmentPermissions_Form)



                                 requestcopy={} #request #.POST.copy()
                                 requestcopy['form-0-user']=user.id
                                 requestcopy['form-0-instituion']=instObj.id
                                 requestcopy['form-0-assessment']=assessmentObj.id
                                 requestcopy['form-TOTAL_FORMS']=1
                                 requestcopy['form-MAX_NUM_FORMS']=1000
                                 requestcopy['form-0-access']=True
                                 requestcopy['form-0-active']=2
                                 asmPermObj = \
                                    UserAssessmentPermissions.objects.filter(user=user,
                                        assessment=assessmentObj,
                                        instituion=instObj).defer('user'
                                        , 'assessment')
                                 if asmPerObj:


                                       requestcopy['form-INITIAL_FORMS']=1
                                       #newrequest.POST=requestcopy
                                       requestcopy['form-0-id']=asmPermObj[0].id
                                       rform = UserPermForm(requestcopy,requestcopy,queryset=asmPerObj)
                                 else:
                                       requestcopy['form-INITIAL_FORMS']=0
                                       #newrequest.POST=requestcopy
                                       rform = UserPermForm(requestcopy,requestcopy)
                                 rform.save()
                                 #asmPermObj[0].access = 1
                                 #asmPermObj[0].save()
                        if reportflag:

                            # To generate Assessment permission report.

                            asmPermObjs = \
                                UserAssessmentPermissions.objects.filter(user=user,
                                    access=1).defer('user', 'assessment'
                                    )
                            objCounter = 0
                            for asmPermObj in asmPermObjs:
                                asmPermData = []
                                boundaryStr = '%s --> %s --> %s' \
                                    % (asmPermObj.instituion.boundary,
                                        asmPermObj.instituion.boundary.parent,
                                        asmPermObj.instituion.boundary.parent.parent)
                                if objCounter == 0:
                                    asmPermData.append(user)
                                else:
                                    asmPermData.append(' ')
                                asmPermData.append(asmPermObj.instituion.name)
                                asmPermData.append(boundaryStr)
                                asmPermData.append(asmPermObj.assessment)
                                asmPermData.append(asmPermObj.assessment.programme)
                                asmPermFile.writerow(asmPermData)
                                objCounter += 1

                        lastprocestime = datetime.datetime.now() \
                            - procestime
                        procestime = datetime.datetime.now()
                        self.stdout.write('      Total time was taken for this user %s'
                                 % str(lastprocestime))
                    self.stdout.write('''
 Total time was taken for all the users %s 
'''
                            % str(datetime.datetime.now() - starttime))
                else:

                         # except IOError:
                    # # If Arguments are not in proper order raises an command error

                    raise CommandError('Pass First Parameter is FileName and Second Parameter is Assessment Id\n'
                            )
        else:

               # except IndexError:
            # If Arguments are not passed raises an command error

            raise CommandError('Pass FileName and Assessment Id\n')


