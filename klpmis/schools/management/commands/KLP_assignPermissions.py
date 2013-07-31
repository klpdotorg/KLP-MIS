#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from klpmis.settings import PROJECT_NAME, PROJECT_ROOT
from django.conf import settings

from schools.models import *
import django
import datetime
import os
import csv
from klprestApi.KLP_Permission import assignPermission
from django.contrib.contenttypes.models import ContentType
from optparse import make_option
from django.db import transaction


def permission_status_message(assessList,assId,index_val):
    if assessList[assId][index_val]:
        perm_list = str(assessList[assId][index_val])
        msg += '\t \t \t No of Institution : ' \
                            + str(len(assessList[assId][index_val])) \
                            + ''': 

      \t \t \t ''' \
                            + perm_list[1:len(perm_list) - 1] \
                            + ''' .

'''
    else:
        msg = ' \t \t \t None . \n\n'
    return msg

class Command(BaseCommand):

        # option_list = BaseCommand.option_list + (make_option('--user', dest='user', type='string',help='User running the command'),)

    @transaction.autocommit
    def handle(self, *args, **options):
        print args, 'options ', options
        if 1:

            # Reads the arguments from command line.

            print 'INNTER TRY',len(args)
            inst_list = args[0]  # options["inst_list"]
            deUserList = args[1]  # options["deUserList"]

            permissionType = args[3]  # options["permissionType"]
            permissions = args[2]  # options["permissions"]
            assessmentId = args[4]  # options["assessmentId"]
            assessmentPerm = args[5]  # options["assessmentPerm"]
            bound_cat = args[6]
            bound_list = args[7]
            username =args[8]
            current_user= args[9]
            path_info=args[10] 
            inst_listall = []
            deUserList = deUserList.split(',')
            permissions = permissions.split(',')
            bound_list = bound_list.split(',')
            print inst_list, bound_cat, bound_list
            asmIdList = []
            if inst_list and bound_cat in ['cluster', 'circle']:
                inst_list = inst_list.split(',')
                inst_listall = inst_list
            else:

                            # asmIdList = assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId, assessmentPerm)

                if bound_cat == 'district':
                    inst_listall = \
                        Institution.objects.filter(boundary__parent__id__in=bound_list,
                            active=2).values_list('id',
                            flat=True).distinct()
                elif bound_cat in ['block', 'project']:
                    inst_listall = \
                        Institution.objects.filter(boundary__id__in=bound_list,
                            active=2).values_list('id',
                            flat=True).distinct()
            (asmIdList, allassignIds, dic) = assignPermission(
                inst_listall,
                deUserList,
                permissions,
                permissionType,
                assessmentId,
                assessmentPerm,username,current_user,path_info
                )
            self.SendingMail(
                asmIdList,
                deUserList,
                permissions,
                permissionType,
                allassignIds,
                assessmentPerm,
                bound_list,
                username,
                dic,
                )
            print 'Successfully Assigned'
        if 0:
            raise CommandError('Pass First Parameter as Boundary Ids List file and Second Parameter as User Ids List \n'
                               )

    def SendingMail(
        self,
        inst_list,
        deUserList,
        permissions,
        permissionType,
        assessmentId,
        assessmentPerm,
        bound_list,
        username,
        dic,
        ):
        inst_list = list(set(inst_list))
        detailmessage = \
            'The following is the Assignment data for the current action only:\n'
        for k in dic:

            detailmessage += '''User name :%s (%d) 
 
 ''' % (k[0],
                    k[1])
            assIds = dic[k][0]
            for assId in assIds:
                assName = Assessment.objects.filter(id=assId)[0].name
                permission_update_status()
                detailmessage += \
                    ''' \t \t Permissions were already assigned to the following institutions for assessment %s :
 
''' \
                    % (str(assId) + '-' + assName)
                detailmessage += permission_status_message(assIds,assId,0)

                detailmessage += \
                    ''' \t \t Permissions were newly assigned to the following institutions for assessment %s :
 
 ''' \
                    % (str(assId) + '-' + assName)
                
                detailmessage += permission_status_message(assIds,assId,1)
            if not assIds:
                detailmessage += \
                    '''\t \t Assessment assigned to the user: None 

'''
            if dic[k][1] or dic[k][2]:
                detailmessage += \
                    ''' \t \t Permissions were newly assigned to the following institutions 

'''

                detailmessage += permission_status_message(dic,k,1)

                detailmessage += \
                    ''' \t \t Permissions were already assigned to the following institutions

 '''
                detailmessage += permission_status_message(dic,k,2)

        inst_liststr = ', '.join(str(x) for x in inst_list)
        boundarystr = ''
        if bound_list != ['']:  # print bound_list,"boundarylist"
            boundarylist = Boundary.objects.filter(id__in=bound_list)

            if bound_list:
                boundarystr = 'Assigned Permissions in \n'
                for k in boundarylist:

                    boundarystr += k.name + '----->' \
                        + k.boundary_category.boundary_category + ',\n'
        sender = settings.REPORTMAIL_SENDER
        receiver = settings.REPORTMAIL_RECEIVER
        subject = \
            'Assigned Permissions for Institutions and Assessments by %s from %s server' \
            % (username, PROJECT_NAME)
        permissionTypetext = ('Assign Permissions' if permissionType
                              == 'permissions'
                               else 'Assessment Permissions')
        assessmentPermtext = ('True' if assessmentPerm not in ['None',
                              None, ''] else 'False')
        fullmsg = \
            '''%s 
 %s  
 User List : %s  
 Admin Action :%s 
 Assessment Id List : %s 
 Assign Assessment checked : %s ''' \
            % (
            boundarystr,
            detailmessage,
            deUserList,
            permissionTypetext,
            assessmentId,
            assessmentPermtext,
            )

        send_mail(subject, fullmsg, sender, receiver)


