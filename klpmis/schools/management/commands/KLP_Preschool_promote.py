#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from datetime import datetime
from klp.settings import *


class Command(BaseCommand):

    # args = '<inst_id inst_id ...>'
    # help = 'Students Promoting to Next Year'

    def handle(self, *args, **options):

        currentAcademic = current_academic
        currentYear = int(currentAcademic().name.split('-')[1])
        nextAcademic = str(currentYear) + '-' + str(currentYear + 1)
        currentAcademicObj = currentAcademic
        print 'CurrentAcademic Year :', current_academic().name
        print 'Next Academic Year  : ', nextAcademic
        nextAcademicObj = \
            Academic_Year.objects.get_or_create(name=nextAcademic)
        nextAcademicObj = (nextAcademicObj if not type(nextAcademicObj)
                           is tuple else nextAcademicObj[0])
        queryStr = \
            """insert into schools_Student_StudentGroupRelation( student_id ,student_group_id ,academic_id,active) (  select student_id ,student_group_id,121,2 from schools_Student_StudentGroupRelation where academic_id=%d and active=2 and student_group_id in (select id from schools_studentgroup where active=2 and institution_id in (select id from  schools_institution where cat_id in (11,10,12) and active=2) and active=2 and group_type='Class'))""" \
            % nextAcademicObj.id
        d = DATABASES['default']
        datebase = d['NAME']
        user = d['USER']
        password = d['PASSWORD']
        connection = psycopg2.connect(database=datebase, user=user,
                password=password)
        cursor = connection.cursor()
        cursor.execute(queryStr)
        cursor.close()

        self.stdout.write('Students Are Promoted ...\n')


