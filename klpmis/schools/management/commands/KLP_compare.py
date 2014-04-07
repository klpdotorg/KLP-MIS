#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from schools.models import *
import datetime
import psycopg2
from django.contrib.contenttypes.models import *
import csv
import os


class Command(BaseCommand):

    # args = '<inst_id inst_id ...>'
    # help = 'Students Promoting to Next Year'

    def handle(self, *args, **options):
        scriptStartTime = datetime.datetime.now()
        filename = args[0]
        dataList=[]
        firstDbDict = {}
        conn_string1 = "host='' dbname='klp_master' user='klp' password='hghykut#$2'"
        conn_string2 = "host='' dbname='emsdev3' user='emsdev3' password='hgfyrtgasw232'"
        conn_string = [(conn_string1, conn_string2)]

        cwd = os.getcwd()
        path = '%s/logFiles/' % cwd

        if not os.path.exists(path):
            os.makedirs(path)

        genFile = '%s/%s.csv' % (path, filename)
        historyFile = csv.writer(open(genFile, 'wb'))
        headerList = ['Master_Database_Student_Group_Names', 'Number_Of_Records','Partition_Database_Student_Group_Names', 'Number_Of_Records','Difference']
        print 'header built'
        historyFile.writerow(headerList)

        db1 = psycopg2.connect(conn_string1) #master database connection
        c1 = db1.cursor()
        q1 = "select id from schools_academic_year where id=%s" %(121)
        c1.execute(q1)
        res1 = c1.fetchall()
        masterAcademicId = res1[0][0]
        db1.close()

        db2 = psycopg2.connect(conn_string2) #test-production database connection
        c2 = db2.cursor()
        q2 = "select id from schools_academic_year where id=%s" %(122)
        c2.execute(q2)
        res2 = c2.fetchall()
        testAcademicId = res2[0][0]
        db2.close()

        groupList = [1,2,3,4,5,6,7,8,9,10] # student group names
        for i, j in conn_string:
            # print the connection string we will use to connect
            #print "Connecting to database\n	->%s" % (i)
            #print "Connecting to database\n	->%s" % (j)
            # get a connection, if a connect cannot be made an exception will be raised here
            conn1 = psycopg2.connect(i)
            cursor1 = conn1.cursor()
            conn2 = psycopg2.connect(j)
            cursor2 = conn2.cursor()
            for k in groupList:
                masterGroupName = k
                testGroupName = k + 1
                # execute master db Query
                q1 = """select count(id) from schools_student_studentgrouprelation where active=%s and academic_id=%s and student_group_id in (select id from schools_studentgroup where name='%s');""" %(2,masterAcademicId,masterGroupName)

                q2 = """select count(id) from schools_student_studentgrouprelation_2 where academic_id=%s and student_group_id in (select id from schools_studentgroup_2 where name='%s');""" %(testAcademicId,testGroupName)

                q3 = """ select count(id) from schools_student_studentgrouprelation_3 where academic_id=%s and student_group_id in (select id from schools_studentgroup_2 where name='%s');""" %(masterAcademicId,10)

                cursor1.execute(q1)
                if testGroupName <= 10:
                    cursor2.execute(q2) # count for group name <= 10
                else:
                    cursor2.execute(q3) # count for group name = 10

                # retrieve the records from the database
                records1 = cursor1.fetchall()
                records2 = cursor2.fetchall()
                diff = int(records2[0][0]) - int(records1[0][0])
                historyFile = csv.writer(open(genFile, 'a'))
                dataList.append(masterGroupName)
                dataList.append(int(records1[0][0]))
                if testGroupName <= 10:
                    dataList.append(testGroupName)
                else:
                    testGroupName = "promoted"
                    dataList.append(testGroupName)
                dataList.append(int(records2[0][0]))
                dataList.append(diff)
                historyFile.writerow(dataList)
                dataList = []
            cursor1.close()
            cursor2.close()
        print '%s.csv file has been created in %s/logFiles directory'\
                         % (filename, cwd)
        tottime = (datetime.datetime.now() - scriptStartTime)
        tot =  "Master database and partition database student groups records count is completed in " + str(tottime) 
        return tot

