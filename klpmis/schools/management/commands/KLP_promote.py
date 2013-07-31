#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
import psycopg2
import pdb
import subprocess

DRY_RUN = 0
def exec_bulk_insert(sqlQuery):
    """Function to execute a command and return stuff"""
    query = "echo \"%s\">klpQuery.txt" % sqlQuery
    p=subprocess.Popen(query,stdout=subprocess.PIPE, shell=True)
    p=subprocess.Popen("psql -fklpQuery.txt klpmis klpmis",stdout=subprocess.PIPE, shell=True)
    (output,err) = p.communicate()
    return output, err
    
  
def promote_tenth_students(academic_id):
    promoteStudentGroupSql = "begin;insert into schools_student_studentgrouprelation_3( student_id,student_group_id, academic_id, active) select student_id,student_group_id, academic_id,3 from schools_student_studentgrouprelation_2 where academic_id = %s and student_group_id in (select id from schools_studentgroup where name='10');commit;" %(academic_id)
    removeStudentGroupSql = "begin;delete from schools_student_studentgrouprelation_2 where academic_id = %s and student_group_id in (select id from schools_studentgroup where name='10');commit;" %(academic_id)

    promoteStudentSql = "begin;insert into schools_student_3(child_id, other_student_id, active) select child_id, other_student_id,3 from schools_student_2 where id in (select student_id from schools_student_studentgrouprelation_2 where academic_id=%s and student_group_id in( select id from schools_studentgroup where name ='10'));commit;"%( academic_id)
    
    removeStudentSql = "begin;delete from schools_student_2 where id in  (select student_id from schools_student_studentgrouprelation_2 where academic_id=%s and student_group_id in( select id from schools_studentgroup where name ='10'));commit;"%( academic_id)
        
    
    #move 10th std to make those studentgroups inactive
    status = exec_bulk_insert(promoteStudentGroupSql)
    if status[1]:
        print "Class Promotion of Tenth std  failed"
    elif not DRY_RUN:
        status = exec_bulk_insert(removeStudentGroupSql)
        if status[1]:
            print "Deletion of Tenth std students from active-table failed"
            
    #move students from 10th std to make them inactive            
    status = exec_bulk_insert(promoteStudentSql)
    if status[1]:
        print "Promotion of Tenth std students failed"
    elif not DRY_RUN:
        status = exec_bulk_insert(removeStudentSql)
        if status[1]:
            print "Class Deletion of Tenth std active-table failed"
        else:
            print "10th std promotion completed!"
    return 1
    
def deactivate_current_year_student_sg_association(academic_id):
    deactivateStudentGroupSql = "begin;insert into schools_student_studentgrouprelation_1( student_id,student_group_id, academic_id, active) select student_id,student_group_id, academic_id,1 from schools_student_studentgrouprelation_2 where academic_id = %s and student_group_id in (select id from schools_studentgroup where name in ('1','2','3','4','5','6','7','8','9'));commit;" %(academic_id)
    removeStudentGroupSql = "begin;delete from schools_student_studentgrouprelation_2 where academic_id = %s and student_group_id in (select id from schools_studentgroup where name in ('1','2','3','4','5','6','7','8','9'));commit;" %(academic_id)      
    
    #make studentgroups inactive
    status = exec_bulk_insert(deactivateStudentGroupSql)
    if status[1]:
        print "Inactivation of student_studentgroups relation for all classes from 1st to 9th failed."
    elif not DRY_RUN:
        status = exec_bulk_insert(removeStudentGroupSql)
        if status[1]:
            print "Removal of inactivated student_studentgroups relation for all classes from 1st to 9th failed"
        else:
            print "All current year's student group relations deactivated!"
    return 1

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
    
def validate_db(db1,currentAcademicYear,nextAcademicYear):
    err_txt = ""
    invalid_nextyear_st_grp_rel_sql = "select * from schools_student_studentgrouprelation_2 where academic_id=%s limit 1"%nextAcademicYear
    result = run_query(db1,invalid_nextyear_st_grp_rel_sql)
    if result:
        err_txt +="[ERROR] studentgroup relation table already has next academic year's records;"
    invalid_curyear_st_grp_rel_sql = "select * from schools_student_studentgrouprelation where academic_id=%s and active in(1,3) limit 1"%(currentAcademicYear)
    result = run_query(db1,invalid_curyear_st_grp_rel_sql)
    if result:
        err_txt +="[ERROR] studentgroup relation table already has current academic year's inactive/ promoted records;"    
    return err_txt
        
def move_class_sql(cur_studentgroup_id,next_studentgroup_id, currentAcademicId, nextAcademicId, sgname=10):


    if  sgname <10:
        
        createNextClassEntriesSql = "begin;insert into schools_student_studentgrouprelation_2(student_id, student_group_id, academic_id, active) select  student_id,%s, %s, 2 from schools_student_studentgrouprelation_1 where academic_id= %s and student_group_id =%s;commit;"%( next_studentgroup_id,nextAcademicId, currentAcademicId,cur_studentgroup_id)

        status = exec_bulk_insert(createNextClassEntriesSql)
        if status[1]:
            print "Class Promotion failed: %s"%(cur_studentgroup_id)
    return 1


class Command(BaseCommand):

    # args = '<inst_id inst_id ...>'
    # help = 'Students Promoting to Next Year'
    
    

    
    def handle(self, *args, **options):
        
        db1 = psycopg2.connect (database="klpmis", user="klpmis", password="hgfyrtgasw232")

        scriptStartTime = datetime.now()
        
        inslist=[]
        currentAcademicYearSql="select id,name from schools_academic_year where active=1"
        currentAcademicYearRec = run_query(db1,currentAcademicYearSql)
        currentAcademicId = currentAcademicYearRec[0][0]
        currentAcademicYearName = currentAcademicYearRec[0][1]
        currentYear = int(currentAcademicYearName.split('-')[1])
        nextAcademicYear = str(currentYear) + '-' + str(currentYear + 1)
        print 'CurrentAcademic Year :', currentAcademicYearName
        print 'Next Academic Year  : ', nextAcademicYear
        
        nextAcademicYearSql="select id,name from schools_academic_year where name='%s'"%(nextAcademicYear)
        nextAcademicRec = run_query(db1,nextAcademicYearSql)
        nextAcademicId = nextAcademicRec[0][0]
        validation_errors = validate_db(db1,currentAcademicId,nextAcademicId)
        if not validation_errors:
            print "DB validated for invalid studentgroup_relation records!!"
            promote_tenth_students(currentAcademicId,)
            deactivate_current_year_student_sg_association(currentAcademicId)
            query1="""select distinct institution_id as id from schools_studentgroup  where id in  (select distinct student_group_id from schools_Student_StudentGroupRelation_1 where academic_id=%s and student_group_id in (select id from schools_studentgroup where active=2 and institution_id in (select id from  schools_institution where cat_id not in (10,11,12) and active=2) and active=2 and group_type='Class')
 ) """%(currentAcademicId)
            print query1
            inst_list = run_query(db1,query1)
            for insobj in inst_list:
                db = psycopg2.connect (database="klpmis", user="klpmis", password="hgfyrtgasw232")
                if 1:
                    instid = insobj[0]
                    insquery = """select id, name from schools_institution where id=%s""" %(instid)
                    insres = run_query(db,insquery)
                    instituteId = insres[0][0]
                    instituteName = insres[0][1]
                    print 'Institution Name : ', instituteId, instituteName
                
                    query2 = """select distinct student_group_id as id from schools_student_studentgrouprelation_1 where academic_id =%s and student_group_id in (select id from schools_studentgroup where active=2 and institution_id =%s and group_type='%s' order by id)"""%(currentAcademicId,instituteId,'Class')
                    sglist = run_query(db,query2)
                    for sg in sglist:
                        totalpromotedStud = 0
                        totalStud = 0
                        sgid=sg[0]
                        try:
                            
                            sgSql= ("select id,name,section from schools_studentgroup where id =%s"%(sgid))
                            sgRec = run_query(db,sgSql)
                            sgname = sgRec[0][1]
                            sgsection = sgRec[0][2]
                            int_sg=int(sgname) # if it fails, then its not a valide class name, so skip and proceed
                            print 'In student group [%s]: %s %s' % (sgid,
                                sgname, sgsection)
                            if int_sg < 10:
                                nxtGroup = int_sg + 1                                
                            nextSgRec = run_query(db,"select id,active from schools_studentgroup where institution_id=%s and name='%s' and section='%s'"%(instituteId, nxtGroup,sgsection))
                            if not nextSgRec:
                                run_query(db,"begin;insert into schools_studentgroup(institution_id, name, section, active, group_type) values(%s, '%s', '%s',2,'Class') ;commit;" %(instituteId, nxtGroup,sgsection))
                                nextSgRec = run_query(db,"select id,name, section from schools_studentgroup where institution_id =%s and name='%s' and  section='%s' and active=2 and group_type='%s' " %(instituteId, nxtGroup,sgsection,'Class'))
                            elif nextSgRec[0][1] !=2:
                                updateSgRec = run_query(db,"begin;update schools_studentgroup set active=2 where institution_id=%s and name='%s' and section='%s';commit;"%(instituteId, nxtGroup,sgsection))
                                    
                            nextSgId = nextSgRec[0][0]
                            move_class_sql(sgid,nextSgId, currentAcademicId, nextAcademicId, int_sg)
                            
                        except:
                            print "Not a valid class name", sgname
                #except:
                #    print "Institution error: %s"%(instid)
                db.close()
            self.stdout.write('Students Are Promoted ...\n')        
        else:
            for err in validation_errors.split(";"):
                print err
        totaltime = datetime.now() - scriptStartTime
        print totaltime
        
        

