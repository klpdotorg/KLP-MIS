from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
#import os
import string
import time
import django, datetime, os, csv
class Command(BaseCommand):
        #option_list = BaseCommand.option_list + (make_option('--user', dest='user', type='string',help='User running the command'),)
        @transaction.autocommit         
	def handle(self, *args, **options):
                runpath="python manage.py"
                exefile = "" 
		try:
			# Reads the arguments from command line.
			prgram=programme=options["scriptname"]
                except:
                        program=programme="KLP_permission.py"  
	        try:   		
        		#time.sleep(6)
                        print args
                        #os.system("python manage.py KLPd "+args[1] +" " +args[2]+" "+args[3]+" "+args[4]+" "+args[5]+" "+args[6])
        		#sv= os.spawnvp(os.P_WAIT,runpath, (programme,) + args)
                        print sv
        		ss=  os.spawnlp(os.P_WAIT, 'python', 'python', 'timesleep.py')
                        print ss
    		except AttributeError:
        		print "EROOR"
    		try:
        		spawnv = os.spawnv
    		except AttributeError:
        		# assume it's unix
        		pid = os.fork()
       	 		if not pid:
            			os.execvp(program, (program,) + args)
        			return os.wait()[0]
    		else:
        			# got spawnv but no spawnp: go look for an executable
        			for path in string.split(os.environ["PATH"], os.pathsep):
            				file = os.path.join(path, program) + exefile
            				try:
                				return spawnv(os.P_WAIT, file, (file,) + args)
            				except os.error:
                				pass
        			raise IOError, "cannot find executable"
	
