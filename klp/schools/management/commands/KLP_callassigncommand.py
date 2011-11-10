from django.core.management.base import BaseCommand, CommandError
from schools.models import *
import django, datetime, os, csv
from klprestApi.KLP_Permission import assignPermission
from django.contrib.contenttypes.models import ContentType
from optparse import make_option
from django.db import transaction
from django.conf import settings
from django.core.management import call_command
from schools.models import *
class Command(BaseCommand):
        #option_list = BaseCommand.option_list + (make_option('--user', dest='user', type='string',help='User running the command'),)
        @transaction.autocommit         
	def handle(self, *args, **options):
                        print args,options               
                        deUserList = options['assignToUser']
       			#get selected permissions list
        		permissions = options['userPermission']
        		# get permission type
        		message="A mail will be sent to team@klp.org.in as soon as all the permissions are assigned"
       			permissionType = options['permissionType']
       			# get assessment Id to assign assessment permissions
       			assessmentId = options['assessmentId']
       			# get boundary category 
       			bound_cat = options['bound_cat']
       			# get selected institutions list
       			inst_list = options['instName']
       			# get selected boundaries list
        		bound_list = options['boundaryName']
        	        respDict={}
			# get assessment permission (True or False)
        		assessmentPerm = options['assessmentPerm']


                        if bound_cat == 'district':
                                # if boundary category is district query for institutions under sub boundaries
                                for bound in bound_list:
                                        inst_list = Institution.objects.filter(boundary__parent__id = bound, active=2).values_list('id', flat=True).distinct()
                                        # get count of institutions to show count of assigned institution objects to user
                                        #count = count + inst_list.count()
                                        # call assignPermission method to assign permissions
                                        #inst_list=','.join(str(v1) for v1 in inst_list if v1 > 0)


                                        call_command("KLP_assignPermissions",verbosity=0,interactive=False,inst_list=inst_list,deUserList=deUserList,permissions=permissions,  permissionType=permissionType,assessmentId=assessmentId, assessmentPerm=assessmentPerm)

                                        #asmIdList = assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId, assessmentPerm)
                                        #assignedAsmIds.extend(asmIdList)
                        elif bound_cat in [ 'block', 'project']:
                                # if boundary category is district query for institutions under sub boundaries
                                for bound in bound_list:
                                        inst_list = Institution.objects.filter(boundary__id = bound, active=2).values_list('id', flat=True).distinct()
                                        # get count of institutions to show count of assigned institution objects to user
                                        #count = count + inst_list.count()
                                        # call assignPermission method to assign permissions
                                        call_command("KLP_assignPermissions",verbosity=0,interactive=False,inst_list=inst_list,deUserList=deUserList,permissions=permissions, permissionType=permissionType, assessmentId=assessmentId, assessmentPerm=assessmentPerm)

                                        #asmIdList = assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId, assessmentPerm)
                                        #assignedAsmIds.extend(asmIdList)
                        if assessmentPerm:
                                assignedAsmIds =  list(set(assignedAsmIds))
                                # get length of assessment ids to show count of assigned assessment objects to user
                                asmCount = len(assignedAsmIds)
                                respDict['respMsg'] = message #'Assigned Permissions successfully for %s Institutions  and %s Assessments Assigned successfully' %(count, asmCount)
                        else:
                                respDict['respMsg'] = message #'Assigned Permissions successfully for %s Institutions' %(count)
                        respDict['isSuccess'] = True
                        Tosendmailteam(inst_list,deUserList,permissions,permissionType,assessmentId,assessmentPerm)



from django.core.mail import send_mail
def Tosendmailteam(inst_list,deUserList,permissions,permissionType,assessmentId,assessmentPerm):
     inst_liststr=''
     if inst_list:
        inst_liststr=', '.join(str(x) for x in inst_list)
     sender=settings.REPORTMAIL_SENDER
     receiver=settings.REPORTMAIL_RECEIVER
     subject="Assigned Permissions for Institutions and Assessments "
     fullmsg="Institutions List : %s \n User List : %s \n Permissions : %s \n Permission Type :%s \n Assessment Id List : %s \n Assessment Permissions : %s " %(inst_liststr,deUserList,permissions,permissionType,assessmentId,assessmentPerm)
     send_mail(subject, fullmsg, sender,receiver)


