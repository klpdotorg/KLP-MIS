

from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from datetime import datetime

class Command(BaseCommand):
    #args = '<inst_id inst_id ...>'
    #help = 'Students Promoting to Next Year'

    def handle(self, *args, **options):
		    
		     
		    currentAcademic = current_academic
		    currentYear = int(currentAcademic().name.split('-')[1])
		    nextAcademic =  str(currentYear)+'-'+ str(currentYear+1)
		    ''' Gets Current Academic Year Object'''
		    currentAcademicObj = currentAcademic   
		    print 'CurrentAcademic Year :',current_academic().name
                    print 'Next Academic Year  : ',nextAcademic 
		    nextAcademicObj = Academic_Year.objects.get_or_create(name=nextAcademic)   
		    nextAcademicObj=nextAcademicObj if not type(nextAcademicObj) is tuple else  nextAcademicObj[0]
		    ''' Fiter For Active Primary School Institutions'''
		    if args:
		         institutions = Institution.objects.filter(id=args[0])
		    else:
		         institutions = Institution.objects.filter(cat__categoryType=1, active=2) 
		    for inst in institutions:
			    ''' Filter For Active StudentGroups Of type Class '''
			    studentGroups = StudentGroup.objects.filter(institution=inst, active=2, group_type="Class").order_by("name").reverse()
			    sgdic= studentGroups.values_list('id','name')
			    sgidlist=dict(((int(k[1]),k[0]) for k in sgdic))
			    sglist=[int(k[1]) for k in sgdic]
			    sglist.sort()
                            sglist.reverse()
			    totalsg=len(sglist)
			    for sgid in sglist:
			       
				        sg=StudentGroup.objects.get(id=sgidlist[sgid])
				        ''' Filter For Active Student And StudentGroup Relation Objects Of Current Academic Year '''
				        sg_stRealtions = Student_StudentGroupRelation.objects.filter(student_group=sg, academic=currentAcademicObj, active=2)
				        '''  school have next class or not .If next class is there ,create or get StudentGroup '''
				        if sglist.index(sgid)!=0:
                                                groupName = sg.name
                                                nxtGroup = int(groupName) + 1
                                                groupSec = sg.section
                                                '''Checks For Next Class With Section of type class. if not there it will create '''
				                nextSg = StudentGroup.objects.get_or_create(institution = inst, name=nxtGroup, section=groupSec, active__in= [0,1,2], group_type="Class")
                                                nextSg=nextSg if not type(nextSg) is tuple else nextSg[0]
                                                '''check next class active or not .if not active ,it will activate'''
                                                if nextSg.active!=2:
				                  nextSg.active=2
				                  nextSg.save()               
						'''Student Group  has student or not .student are not there ,deactive the student group else promote the student'''
						if sg_stRealtions:
						    for sg_st in sg_stRealtions:
						                studentObj = sg_st.student
						                '''Checks For Next Class With Section of type class. If it There map with student for next academic else pass'''
	      					                nxt_Sg_relation = Student_StudentGroupRelation.objects.get_or_create(student_group=nextSg, student=studentObj, academic=nextAcademicObj , active=2)
						else:
                                                    '''No students are there ,student group will be deactivated'''
                                                    sg_stRealtions.update(active=1)
						    sg.active=1 #Not clear it should be delete 0 or inactive 1
						    sg.save()
		                        else:
                                          '''It student group is final ,change the action to 4 .that means all promoted from school'''
                                          
                                          
		                          sg_stRealtions.update(active=4)
		    self.stdout.write('Students Are Promoted ...\n')
		    '''To find the all current year programees'''
		    prog=Programme.objects.filter(endDate__range=[datetime.strptime(str(currentYear)+'-06-01','%Y-%m-%d'),datetime.strptime(str(currentYear+1)+'-05-31','%Y-%m-%d')])
		    #assement=Assessment.objects.filter(programme__in=prog)
		    prog.update(active=1)
		    print prog
		    self.stdout.write('Programmes are inActivated ...\n') 
