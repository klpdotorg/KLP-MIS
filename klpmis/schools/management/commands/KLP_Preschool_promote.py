#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from datetime import datetime
import psycopg2
import subprocess


def exec_bulk_insert(sqlQuery):
    """Function to execute a command and return stuff"""
    query = "echo \"%s\">klpQuery.txt" % sqlQuery
    p=subprocess.Popen(query,stdout=subprocess.PIPE, shell=True)
    p=subprocess.Popen("psql -fklpQuery.txt klpmis klpmis",stdout=subprocess.PIPE, shell=True)
    (output,err) = p.communicate()
    return output, err

def run_query(db,sql):
    db = psycopg2.connect (database="klpmis", user="klpmis", password="hgfyrtgasw232")
    cursor1 = db.cursor()
    cursor1.execute(sql)
    recs=""
    try:
        recs = cursor1.fetchall()
    except:
        db.commit()
    cursor1.close()
    return recs


def move_class_sql(currentAcademicId, nextAcademicId):


    preSchooolPromoteSql = \
            """insert into schools_Student_StudentGroupRelation_2( student_id ,student_group_id ,academic_id,active) (  select student_id ,student_group_id,%s, 2 from schools_Student_StudentGroupRelation_2 where academic_id=%s and student_group_id in (select id from schools_studentgroup_2 where institution_id in (select id from  schools_institution where cat_id in (11,10,12) and active=2)  and group_type='Class'))""" \
            % (nextAcademicId,currentAcademicId)

    preSchoolMoveInactivateSql = """insert into schools_Student_StudentGroupRelation_1( student_id ,student_group_id ,academic_id,active) (  select student_id ,student_group_id,academic_id, 1 from schools_Student_StudentGroupRelation_2 where academic_id=%s and student_group_id in (select id from schools_studentgroup_2 where institution_id in (select id from  schools_institution where cat_id in (11,10,12) and active=2)  and group_type='Class'))""" \
            % (currentAcademicId)

    preSchoolDeleteSql = """delete from schools_Student_StudentGroupRelation_2 where academic_id=%s and student_group_id in (select id from schools_studentgroup_2 where institution_id in (select id from  schools_institution where cat_id in (11,10,12) and active=2)  and group_type='Class')""" \
            % (currentAcademicId)

    status = exec_bulk_insert(preSchooolPromoteSql)
    if status[1]:
        print "Class Promotion failed: %s"%(currentAcademicId)

    status = exec_bulk_insert(preSchoolMoveInactivateSql)
    if status[1]:
        print "Class Move failed: %s"%(currentAcademicId)


    status = exec_bulk_insert(preSchoolDeleteSql)
    if status[1]:
        print "Class Deletion failed: %s"%(currentAcademicId)
    return 1


class Command(BaseCommand):

    # args = '<inst_id inst_id ...>'
    # help = 'Students Promoting to Next Year'

    def handle(self, *args, **options):

        scriptStartTime = datetime.now()

        db1 = psycopg2.connect (database="klpmis", user="klpmis", password="hgfyrtgasw232")
        curAcObj = current_academic()
        currentAcademicYearSql="select id,name from schools_academic_year where id=%s" %(curAcObj.id)
        
        currentAcademicYearRec = run_query(db1,currentAcademicYearSql)
        currentAcademicId = currentAcademicYearRec[0][0]
        currentAcademicYearName = currentAcademicYearRec[0][1]
        currentYear = int(currentAcademicYearName.split('-')[1])
        nextAcademicYear = str(currentYear) + '-' + str(currentYear + 1)
        print 'CurrentAcademic Year :', currentAcademicYearName
        print 'Next Academic Year  : ', nextAcademicYear
        
        nextAcademicYearSql="select id,name from schools_academic_year where name='%s'"%(nextAcademicYear)
        print nextAcademicYearSql
        nextAcademicRec = run_query(db1,nextAcademicYearSql)
        nextAcademicId = nextAcademicRec[0][0]

        move_class_sql(currentAcademicId, nextAcademicId)
        totaltime = datetime.now() - scriptStartTime
        print totaltime
        print 'preschool students have been Promoted to ' ,nextAcademicYear


