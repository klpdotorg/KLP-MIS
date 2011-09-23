from django.core.management.base import BaseCommand, CommandError
from schools.models import *
import datetime

class Command(BaseCommand):
    #args = '<inst_id inst_id ...>'
    #help = 'Students Promoting to Next Year'

    def handle(self, *args, **options):
    	now = datetime.date.today()
	currentYear = int(now.strftime('%Y'))
	currentAcademic = '%s-%s' %(currentYear-1, currentYear)
	nextAcademic = '%s-%s' %(currentYear, currentYear+1)
	''' Gets Current Academic Year Object'''
	currentAcademicObj = Academic_Year.objects.get(name=currentAcademic)       
	try:
		''' Checks For Next Academic Year Object'''
		nextAcademicObj = Academic_Year.objects.get(name=nextAcademic)     
	except Academic_Year.DoesNotExist:
		''' If Not Found Creates Next Academic Year Object'''
		nextAcademicObj = Academic_Year(name = nextAcademic)		   
		nextAcademicObj.save()
	''' Fiter For Active Primary School Institutions''' 
    	institutions = Institution.objects.filter(cat__categoryType=1, active=2)   
    	
    	for inst in institutions:
    		''' Filter For Active StudentGroups Of type Class '''
    		studentGroups = StudentGroup.objects.filter(institution=inst, active=2, group_type="Class").order_by("name").reverse()
    		
    		for sg in studentGroups:
    			''' Filter For Active Student And StudentGroup Relation Objects Of Current Academic Year '''
    			sg_stRealtions = Student_StudentGroupRelation.objects.filter(student_group=sg, academic=currentAcademicObj, active=2)
    			for sg_st in sg_stRealtions:
    				studentObj = sg_st.student
    				sg_st.active = 3
    				sg_st.save()
				groupName = sg.name
				nxtGroup = int(groupName) + 1
				groupSec = sg.section
							
				if groupSec == 'A':
					''' If Section Is 'A' do Following'''
					try:
						'''Checks For Next Class With Section of type class. If it There map with student for next academic else pass'''
						nextSg = StudentGroup.objects.get(institution = inst, name=nxtGroup, section=groupSec, active=2, group_type="Class")
						nxt_Sg_relation = Student_StudentGroupRelation(student_group=nextSg, student=studentObj, academic=nextAcademicObj , active=2)
						nxt_Sg_relation.save()
								
							
					except StudentGroup.DoesNotExist:
						pass
				else:
					''' If Section Is Not 'A' do Following'''
					try:
						'''Checks For Next Class With Section of type class. If it There map with student for next academic '''
						nextSg = StudentGroup.objects.get(institution = inst, name=nxtGroup, section=groupSec, active=2, group_type="Class")
						nxt_Sg_relation = Student_StudentGroupRelation(student_group=nextSg, student=studentObj, academic=nextAcademicObj , active=2)
						nxt_Sg_relation.save()
					except StudentGroup.DoesNotExist:
						''' Else Checks Same Class With Section A. If it finds Checks for deactivated Class With particular Section.'''
						nextSg_A = StudentGroup.objects.get(institution = inst, name=nxtGroup, section='A', active=2, group_type="Class")
						if nextSg_A:
							try:
								''' If Deactivated Class found, activate the class and map the student'''
								deActiveObj = StudentGroup.objects.get(institution = inst, name=nxtGroup, section=groupSec, active=0, group_type="Class")
								deActiveObj.active = 2
								nxt_Sg_relation = Student_StudentGroupRelation(student_group=deActiveObj, student=studentObj, academic=nextAcademicObj , active=2)
								nxt_Sg_relation.save()
							except StudentGroup.DoesNotExist:
								''' If Deactivated Class not found, create new class and map the student'''
								newSgObj = StudentGroup(institution = inst, name=nxtGroup, section=groupSec, active=2, group_type="Class")
								newSgObj.save()
								nxt_Sg_relation = Student_StudentGroupRelation(student_group=newSgObj, student=studentObj, academic=nextAcademicObj , active=2)
								nxt_Sg_relation.save()
						else:
							pass
				currentSgList = StudentGroup.objects.filter(institution = inst, name=groupName, active=2, group_type="Class")
				nxtSgList = StudentGroup.objects.filter(institution = inst, name=nxtGroup, active=2, group_type="Class")
				''' If next Class has more Sections than current Class, then deactivate particular sections'''
				if len(currentSgList) < len(nxtSgList):
					for nxtSg in nxtSgList:
						try:									
							currentSg = StudentGroup.objects.get(institution = inst, name=groupName, section=nxtSg.section, active=2, group_type="Class")
						except StudentGroup.DoesNotExist:
							nxtSg.active = 0
							nxtSg.save()
										
									
    							
    				
    	self.stdout.write('Students Are Promoted ...\n')





