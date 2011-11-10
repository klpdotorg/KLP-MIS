from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

from django.conf import settings

from schools.models import *
import django, datetime, os, csv
from klprestApi.KLP_Permission import assignPermission
from django.contrib.contenttypes.models import ContentType
from optparse import make_option
from django.db import transaction
class Command(BaseCommand):
        #option_list = BaseCommand.option_list + (make_option('--user', dest='user', type='string',help='User running the command'),)
        @transaction.autocommit         
	def handle(self, *args, **options):
                print args,"options ",options                
	        if 1:	

			# Reads the arguments from command line.
                        print "INNTER TRY" 
                        inst_list= args[0] #options["inst_list"]
			deUserList=args[1] #options["deUserList"]

                        permissionType=args[3] #options["permissionType"]        
			permissions=args[2] #options["permissions"]
			assessmentId=args[4] #options["assessmentId"]
			assessmentPerm=args[5] #options["assessmentPerm"]
                        bound_cat=args[6]
                        bound_list=args[7]
                        username=args[8]
                        inst_listall=[]
                        deUserList=deUserList.split(',')
                        permissions=permissions.split(',')
                        bound_list=bound_list.split(',') 
                        print inst_list,bound_cat,bound_list
                        asmIdList=[]
                        if inst_list and bound_cat in ['cluster','circle']:
                            inst_list=inst_list.split(',')
                            inst_listall=inst_list 
                            asmIdList = assignPermission(inst_list, deUserList, permissions, permissionType, assessmentId, assessmentPerm)  
                        else:
                                  for bound in bound_list:
                                     bound=int(bound)
                                     print bound
                                     if bound_cat== 'district':
                                              inst_list = Institution.objects.filter(boundary__parent__id = bound, active=2).values_list('id', flat=True).distinct()
                                         
                                     elif bound_cat in [ 'block', 'project']:
                                                  inst_list = Institution.objects.filter(boundary__id = bound, active=2).values_list('id', flat=True).distinct()
		              	     inst_listall.extend(inst_list)   
                                  asmIdList = assignPermission(inst_listall, deUserList, permissions, permissionType, assessmentId, assessmentPerm)
                        self.SendingMail(asmIdList,deUserList,permissions,permissionType,assessmentId,assessmentPerm,bound_list,username)
                        print "Successfully Assigned"
		if 0:
			raise CommandError('Pass First Parameter as Boundary Ids List file and Second Parameter as User Ids List \n')
	           		
	def SendingMail(self,inst_list,deUserList,permissions,permissionType,assessmentId,assessmentPerm,bound_list,username):
                        inst_list=list(set(inst_list))     
                        inst_liststr=', '.join(str(x) for x in inst_list)
                        boundarystr=''
                        if bound_list!=['']: #print bound_list,"boundarylist"
                          boundarylist=Boundary.objects.filter(id__in=bound_list)   
                           
                          if bound_list:
                            boundarystr="Assigned Permissions in "
                            for k in boundarylist:
                                         
                                  boundarystr+=k.name+"----->"+k.boundary_category.boundary_category+",\n"
                        sender=settings.REPORTMAIL_SENDER
                        receiver=settings.REPORTMAIL_RECEIVER
                        subject="Assigned Permissions for Institutions and Assessments by %s" % (username)
                        fullmsg="%s \n Institutions List (%s): %s \n User List : %s \n Permissions : %s \n Permission Type :%s \n Assessment Id List : %s \n Assessment Permissions : %s " %(boundarystr,str(len(inst_list)),inst_liststr,deUserList,permissions,permissionType,assessmentId,assessmentPerm)
                        send_mail(subject, fullmsg, sender,receiver)

