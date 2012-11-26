from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from datetime import datetime
from klp.settings import *
class Command(BaseCommand):
    #args = '<inst_id inst_id ...>'
    #help = 'Students Promoting to Next Year'

    def handle(self, *args, **options):
		    
		     
		    currentAcademic = current_academic
		    current_year = int(currentAcademic().name.split('-')[1])
		    nextAcademic =  str(current_year)+'-'+ str(current_year+1)
		    ''' Gets Current Academic Year Object'''
		    currentAcademicObj = currentAcademic   
		    print 'CurrentAcademic Year :',current_academic().name
                    print 'Next Academic Year  : ',nextAcademic 
		    nextAcademicObj = Academic_Year.objects.get_or_create(name=nextAcademic)   
		    nextAcademicObj=nextAcademicObj if not type(nextAcademicObj) is tuple else  nextAcademicObj[0]
                    queryStr="""insert into schools_Student_StudentGroupRelation( student_id ,student_group_id ,academic_id,active) (  select student_id ,student_group_id,121,2 from schools_Student_StudentGroupRelation where academic_id=%d and active=2 and student_group_id in (select id from schools_studentgroup where active=2 and institution_id in (select id from  schools_institution where cat_id in (11,10,12) and active=2) and active=2 and group_type='Class'))""" % (nextAcademicObj.id)
                    d=DATABASES['default']
                    datebase=d['NAME']
                    user=d['USER']
                    password=d['PASSWORD']
                    connection = psycopg2.connect(database=datebase, user=user, password=password)
                    cursor = connection.cursor()
                    cursor.execute(queryStr)
                    cursor.close()
                    
                    """
		    ''' Fiter For Active Pre School Institutions'''
		    if args:
		         institutions = Institution.objects.filter(id=args[0],cat__category_type=2, active=2)
		    else:
		         institutions = Institution.objects.filter(cat__category_type=2, active=2)
		    ''' Filter For Active StudentGroups Of type Class '''
		    studentGroups = StudentGroup.objects.filter(institution__in=institutions, active=2, group_type="Class") 
		    ''' Filter For Active Student And StudentGroup Relation Objects Of Current Academic Year '''
		    sg_stRealtions = Student_StudentGroupRelation.objects.filter(student_group__in=studentGroups, academic=currentAcademicObj, active=2)
		    ''' Filter For Active Student And StudentGroup Relation Objects Of Next Academic Year '''
                    print len(sg_stRealtions)			    
		    if 1: #for sg in studentGroups:
                            for sg_st in sg_stRealtions:
		                                                print "In student group [%s]: %s %s"%(sg.id, sg.name,sg.section)
		                                                sg=sg_st.student_group
						                studentObj = sg_st.student
						                '''Checks For Next Class With Section of type class. If it There map with student for next academic else pass'''
	      					                nxt_Sg_relation = Student_StudentGroupRelation.objects.get_or_create(student_group=sg, student=studentObj, academic=nextAcademicObj )
                                                                nxt_Sg_relation=nxt_Sg_relation if not type(nxt_Sg_relation) is tuple else nxt_Sg_relation[0]
	      					                nxt_Sg_relation.active =2
	      					                nxt_Sg_relation.save()
	      					               
	      					                print "Student %s promoted from %s to %s" %(studentObj,sg.id,sg)
		    ''' Filter For Deactive Student And StudentGroup Relation Objects Of Current Academic Year '''
		    sg_stRealtions.update(active=1)"""
                    
		    self.stdout.write('Students Are Promoted ...\n')
