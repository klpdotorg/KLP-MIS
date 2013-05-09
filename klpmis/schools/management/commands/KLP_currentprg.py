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
		prvPrgList = Programme.objects.filter(active=2).exclude(Q(endDate__year=currentYear) | Q(endDate__year=currentYear+1))
		for prvPrg in prvPrgList:
			prvPrg.active = 7
			prvPrg.save()
		nxtPrgList = Programme.objects.filter(active=2).exclude(Q(endDate__year=currentYear))	
		for nxtPrg in nxtPrgList:
			nxtPrg.active = 1
			nxtPrg.save()
		if prvPrgList.count():
			self.stdout.write('Previous Academic year Programmes status has been changed to completed...\n')
