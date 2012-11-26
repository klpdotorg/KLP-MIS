from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from django.contrib.contenttypes.models import ContentType
from fullhistory.models import FullHistory
from django.db.models import Q
from django.contrib.auth.models import User
import django, datetime, os, csv
from klp.settings import *
import psycopg2

class Command(BaseCommand):
        ''' Command To generate Data Entry Operators History in csv format.'''
        def handle(self, *args, **options):
                      #b=Boundary.objects.filter(boundary_type=2)
                      #inst=Institution.objects.filter(boundary__in=b)
                      #SGIlist=Child.objects.raw(""" SELECT "id","dob" FROM "public"."schools_child" """) #StudentGroup.objects.filter(institution__in=inst,name='1').distinct()
                      queryStr="select dob from schools_child"
                      #SGIlist.update(name='Anganwadi Class')  
                      d=DATABASES['default']
                      datebase=d['NAME']
                      user=d['USER']
                      password=d['PASSWORD']
                      connection = psycopg2.connect(database=datebase, user=user, password=password)
                      cursor = connection.cursor()
                      cursor.execute(queryStr) 
                      j=0       
                      for sgs in cursor.fetchall():
                            if j==2:
                                j+=1
                                sg=sgs[0]
                                dob=sg.dob
                                if dob:
                                 try:
                                           datetime.datetime(dob,'%Y-%m-%d') 
                                 except:
                                    print str(sg.id)+'--->'+str(dob) 
