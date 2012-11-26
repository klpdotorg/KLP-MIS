from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from django.contrib.contenttypes.models import ContentType
from fullhistory.models import FullHistory
from django.db.models import Q
from django.contrib.auth.models import User
import django, datetime, os, csv
from settings import *
import psycopg2

class Command(BaseCommand):
        ''' Command To generate Data Entry Operators History in csv format.'''
        def handle(self, *args, **options):
                      #b=Boundary.objects.filter(boundary_type=2)
                      #inst=Institution.objects.filter(boundary__in=b)
                      #SGIlist=StudentGroup.objects.filter(institution__in=inst,name='1').distinct()
                      SGIlist=[]
                      queryStr="update schools_answer set content_type_id=29 where id=4469059"
                      #SGIlist.update(name='Anganwadi Class')  
                      d=DATABASES['default']
                      datebase=d['NAME']
                      user=d['USER']
                      password=d['PASSWORD']
                      connection = psycopg2.connect(database=datebase, user=user, password=password)
                      cursor = connection.cursor()
                      cursor.execute(queryStr)         
                      for sg in SGIlist:
                                sgid=sg.id
                                queryStr="update schools_studentgroup set name='Anganwadi Class' where id=%d " % (sgid)
                                try:
                                            cursor.execute(queryStr)
                                except:
                                    print 'Student Group ---->'+str(sgid) +' Insittution --->'+str(sg.institution.id)+','+sg.institution.name
                      cursor.close()                           
