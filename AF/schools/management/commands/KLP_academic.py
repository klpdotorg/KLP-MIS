from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from django.contrib.contenttypes.models import ContentType
from fullhistory.models import FullHistory
from django.db.models import Q 
from django.contrib.auth.models import User
import django, datetime, os, csv



class Command(BaseCommand):
	''' Command To generate Data Entry Operators History in csv format.'''
        def handle(self, *args, **options):
                now = datetime.date.today()
		currentYear = int(now.strftime('%Y'))
		currentAcademic = '%s-%s' %(currentYear-1, currentYear) # get current academic
		nextAcademic = '%s-%s' %(currentYear, currentYear+1)    # get next academic
		try:
			''' Checks For Next Academic Year Object'''
			nextAcademicObj = Academic_Year.objects.get(name=nextAcademic) 
			nextAcademicObj.active = 2
			nextAcademicObj.save()
		except Academic_Year.DoesNotExist:
			''' If Not Found Creates Next Academic Year Object'''
			nextAcademicObj = Academic_Year(name = nextAcademic, active=2)		   
			nextAcademicObj.save()
			
		academicObjects = Academic_Year.objects.filter(active=2).exclude(name=nextAcademic)
		for acObj in academicObjects:
			acObj.active = 0
			acObj.save()
		self.stdout.write('New Academic year is activated/created and Old academics are deactivated...\n')
		
			
