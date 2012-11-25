

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
			    studentGroups = StudentGroup.objects.filter(institution=inst, active__in=[1,2], group_type="Class").order_by("name").reverse()
			    sgdic= studentGroups.values_list('id','name')
			    sgidlist={}
			    for k in sgdic:
  				 if sgidlist.has_key(int(k[1])):
      					val= sgidlist[int(k[1])]
      					val.append(k[0])
   				 else:
     					 val=[k[0]]
   				 sgidlist[int(k[1])]=val
			   
			    sglist=list(set([int(k[1]) for k in sgdic]))
			    sglist.sort()
                            sglist.reverse()
			    totalsg=len(sglist)
			    for sgid in sglist:
			        for k in sgidlist[sgid]:
			        
				        sg=StudentGroup.objects.get(id=k) 
				        print "In student group [%s]: %s %s"%(sg.id, sg.name,sg.section)
				        ''' Filter For Active Student And StudentGroup Relation Objects Of Current Academic Year '''
				        sg_stRealtions = Student_StudentGroupRelation.objects.filter(student_group=sg, academic=currentAcademicObj, active=2)
				        '''  school have next class or not .If next class is there ,create or get StudentGroup '''
				        if sglist.index(sgid)!=0:
                                                groupName = sg.name
                                                nxtGroup = int(groupName) + 1
                                                groupSec = sg.section
				                #print "In student group [%s]: %s %s"%(sg.id, sg.name,sg.section)

						if sg_stRealtions:
                                                	'''Checks For Next Class With Section of type class. if not there it will create '''
				                	nextSg = StudentGroup.objects.get_or_create(institution = inst, name=nxtGroup, section=groupSec, active__in= [0,1,2], group_type="Class")
                                                	nextSg=nextSg if not type(nextSg) is tuple else nextSg[0]
                                                	#print groupSec,groupName						
						    	''' if current yeas student group has students, then before you promote them to next year frst make their student group active fro next year '''
			                                nextSg.active=2
			                                nextSg.save()  
					                print "Next year student group [%s] activated" %(sg.id)  
						            
						    	for sg_st in sg_stRealtions:
						                studentObj = sg_st.student
						                '''Checks For Next Class With Section of type class. If it There map with student for next academic else pass'''
	      					                nxt_Sg_relation = Student_StudentGroupRelation.objects.get_or_create(student_group=nextSg, student=studentObj, academic=nextAcademicObj )
	      					                nxt_Sg_relation.active =2
	      					                nxt_Sg_relation.save()
	      					                sg_st.active=1 #
	      					                sg_st.save()
	      					                print "Student %s promoted from %s to %s" %(studentObj,sgid,nextSg)
						else:
                                                    '''No students are there ,student group will be deactivated'''
                                                    sg_stRealtions.update(active=1)
					            '''sg.active=1 #inactive 1
					            sg.save()
					            print "Current student group [%s] deactivated" %(sg.id)'''
                                                    
						            
		                        else:
                                          '''It student group is final ,change the action to 4 .that means all promoted from school'''
                                          
                                          
		                          sg_stRealtions.update(active=4)
                                  
		    self.stdout.write('Students Are Promoted ...\n')
		    '''To find the all current year programees'''
		    prog=Programme.objects.filter(endDate__range=[datetime.strptime(str(currentYear)+'-06-01','%Y-%m-%d'),datetime.strptime(str(currentYear+1)+'-05-31','%Y-%m-%d')])
		    #assement=Assessment.objects.filter(programme__in=prog)
		    prog.update(active=1)
		    
		    self.stdout.write('Programmes are inActivated ...\n') 
