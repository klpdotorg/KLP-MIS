from django.core.management.base import BaseCommand, CommandError
from schools.models import *
import django, datetime, os, csv
from django.db.models import Q 

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
	cwd = os.getcwd()
	path = "%s/logFiles/" %(cwd)
        if not os.path.exists(path):
        	# if dir not exists creates directory with name logfiles in cwd.
                os.makedirs(path)
        # create csv file with the name passed.    
        fileName = "promotion %s" %(datetime.date.today().strftime("%d-%m-%Y"))    
	genFile = "%s/%s.csv" %(path, fileName)
	logFile = csv.writer(open(genFile, 'wb'))
	
	logFile.writerow(["student_id", "studentgroup", "Instituion", "Boundaries"])
	
    	institutions = Institution.objects.filter(boundary__boundary_type__id=2, active=2)
    	for inst in institutions:
    		''' Filter For Active StudentGroups Of type Class '''
    		studentGroups = StudentGroup.objects.filter(institution=inst, active=2, group_type="Class").order_by("name").reverse()
    		
    		for sg in studentGroups:
    			''' Filter For Active Student And StudentGroup Relation Objects Of Current Academic Year '''
    			sg_stRealtions = Student_StudentGroupRelation.objects.filter(student_group=sg, academic=currentAcademicObj, active=2)
    			for sg_st in sg_stRealtions:
    				studentObj = sg_st.student
    				groupName = sg.name
				nxtGroup = int(groupName) + 1
				groupSec = sg.section
				try:
					'''Checks For Next Class With Section of type class. If it There map with student for next academic else pass'''
					nextSg = StudentGroup.objects.get(institution = inst, name=nxtGroup, section=groupSec, active=2, group_type="Class")
					nxt_Sg_relation = Student_StudentGroupRelation(Q(active=2) | Q(active=4), student_group=nextSg, student=studentObj, academic=nextAcademicObj)
					nxt_Sg_relation.save()
					sg_st.active = 3 # student promoted 
					sg_st.save()								
				except StudentGroup.DoesNotExist:
					studentObj.active = 4 # student promotion fail
					bName = "%s,%s,%s" %(sg.institution.boundary, sg.institution.boundary.parent, sg.institution.boundary.parent.parent)
					logFile.writerow([studentObj.id, sg.name, sg.institution.name, bName])
														
									
    							
    				
    	self.stdout.write('Students Are Promoted and Failed Students data stored in logged File...\n')





