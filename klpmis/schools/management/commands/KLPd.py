from django.core.management.base import BaseCommand, CommandError
from schools.models import *
import django, datetime, os, csv
from klprestApi.KLP_Permission import assignPermission
from django.contrib.contenttypes.models import ContentType
from optparse import make_option
from django.db import transaction
from django.conf import settings
from django.core import management
class Command(BaseCommand):
        #option_list = BaseCommand.option_list + (make_option('--user', dest='user', type='string',help='User running the command'),)
        @transaction.autocommit         
	def handle(self, *args, **options):
                #print settings.REPORT_MAIL,args,"fdfsdf fsdfsdfsdfsdfsd"
                print args  
                #vv=os.spawnvp(os.P_WAIT,"python manage.py", ("KLP_callassigncommand",) + args)
                #print vv 
                management.call_command("KLP_callassigncommand", assignToUser=[u'71', u'72'] ,userPermission=[u'Acess'], permissionType='permissions', assessmentId=" " ,bound_cat="district", instName=[] ,boundaryName=[u'9495'] ,assessmentPerm=None)
                                    
