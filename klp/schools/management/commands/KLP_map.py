from django.core.management.base import BaseCommand, CommandError
from schools.models import *
import django, datetime, os, csv
from klprestApi.TreeMenu import KLP_assignedInstitutions
import datetime
from django.db import transaction
class Command(BaseCommand):
	''' Command To map assessments with student group and to assign permissions to users automatically. And then it list out the user permissions.''' 
        @transaction.autocommit 
	def handle(self, *args, **options):
		try:
			# Reads the arguments from command line.
			fileName = args[0]
			assessment_id = args[1]
                        try:
                               reportflag=args[2]
                        except:
                                    reportflag=0        
			# checks for arguments
                        starttime=procestime=datetime.datetime.now()
                        self.stdout.write('The mapping is started at %s\n' %(starttime))
                        asstypedic={1:'Institution',2:'Student',2:'Student Group'}
			if fileName and assessment_id:
				try:
					mapFile = open(fileName, 'r')  # open file to read data
					studenGroups = mapFile.read().replace('\n', '')  # read data from file
					mapFile.close()   	       # Close file after reading data
					sgList = studenGroups.split(',')  #  splits student group ids by ,
					assessmentObj = Assessment.objects.filter(id=assessment_id).defer('programme')[0]  # get assessment object.
					# get assessment list under programme to assign permissions to user.
					prgObj = assessmentObj.programme
                                        Asstype=assessmentObj.typ              
                                           
					assessment_list = Assessment.objects.filter(programme=prgObj, active=2).defer('programme').values_list("id", flat=True).distinct()
					inst_list = []
					for sg in sgList:
                                            
					    if sg: 
                                                if assessmentObj.typ in [2,3]:            
                                                   errormsg='%s student Group id does not exist ' % (sg)
                                                   sgObj = StudentGroup.objects.filter(id=int(sg)).defer('institution')
                                                   if sgObj:
                                                                sgObj=sgObj[0]          # get student group object
					                        inst_list.append(sgObj.institution.id)
                                                else:
                                                                               errormsg='%s Institution id does not exist ' % (sg)
                                                                               sgObj=Institution.objects.filter(id=int(sg)).defer("boundary","cat","mgmt","inst_address")
                                                                               if sgObj:
                                                                                           sgObj=sgObj[0]             
                                                                                           inst_list.append(int(sg))
                                                if sgObj:
                                                         if assessmentObj.typ==3:                   
                                     				# mapping assesment and student group
				                     		mapObj = Assessment_StudentGroup_Association(assessment = assessmentObj, student_group=sgObj, active=2)
                                                                MappingStr='%s - Assessment and StudentGroup - %s%s ...\n'%(assessmentObj.name, sgObj.name, sgObj.section)
						         elif assessmentObj.typ==2:
                                                                # mapping assesment and student group
                                                                mapObj = Assessment_Class_Association(assessment = assessmentObj, student_group=sgObj, active=2)
                                                                MappingStr='%s - Assessment and StudentGroup - %s%s ...\n'%(assessmentObj.name, sgObj.name, sgObj.section)
                                                         else:
                                                                #mapping assement and Institution
                                                                mapObj = Assessment_Institution_Association(assessment = assessmentObj, institution=sgObj, active=2)
                                                                MappingStr='%s - Assessment and Institution %s ...\n'%(assessmentObj.name, sgObj.name)                           
		         				 try:
			            				mapObj.save()
				              			self.stdout.write('%s are Mapped ...\n'%(MappingStr))
					        	 except django.db.utils.IntegrityError:
                                                               django.db.connection._rollback() 
						               self.stdout.write('%s are Already Mapped ...\n'%(MappingStr))
                                                else:
                                                          self.stdout.write('\n %s ' % (errormsg))
					# get users to assign permissions		
					users_List =  User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'], is_active=1).defer('groups')
					inst_list = list(set(inst_list))
                                        if reportflag:
				     	  cwd = os.getcwd()
					  path = "%s/logFiles/" %(cwd)
					  if not os.path.exists(path):
						os.makedirs(path)
					  instPermCsv = "%s/%s.csv" %(path, 'instpermissions')				
					  instPermFile = csv.writer(open(instPermCsv, 'wb'))
					  asmPermCsv = "%s/%s.csv" %(path, 'assessmentPermissions')
					  asmPermFile = 	csv.writer(open(asmPermCsv, 'wb'))
					  instPermFile.writerow(['User', 'Institutions', 'Boundaries'])
					  asmPermFile.writerow(['User', 'Institutions', 'Boundaries', 'Assessment', 'Programme'])
                                        self.stdout.write('Total No of User %s \n' %(  len(users_List)))
                                        userNo=1
                                        self.stdout.write('Total No Of Institution for Assessment %s \n ' %(len(inst_list)))                                        
					for user in users_List:
                                                # get institutions assigned to user to generate report and to verify user permission.
                                                self.stdout.write("\n%s .Now performing %s ," % ( str(userNo),user.username))
                                                print user.username
                                                perm_instList = KLP_assignedInstitutions(user.id)
                                                perm_instSet=list(set(inst_list).intersection(set(perm_instList)))
                                                InsObjs=Institution.objects.filter(id__in=perm_instSet).defer("boundary","cat","mgmt","inst_address")
                                                TotalInst=InsObjs.values_list("id", flat=True).distinct()
                                                self.stdout.write(" Total Institution %s is assigned to %s" %( len(TotalInst),user.username))    
						asmPerm = []
                                                 
                                                userNo+=1
						# get user permissions in progr
						permObjs = UserAssessmentPermissions.objects.filter(user=user, assessment__id__in=assessment_list, access=1).defer('user','assessment')
						if len(permObjs) >= 1:
									asmPerm.append(True)
						lenTrue = asmPerm.count(True)
						lenAsm = len(assessment_list)
                                                """      
						# get institutions assigned to user to generate report and to verify user permission.
						perm_instList = KLP_assignedInstitutions(user.id)
                                                inscount=0  
                                                InsObjs=Institution.objects.filter(id__in=perm_instList)   
                                                self.stdout.write("%s .Now performing %s ,Total Institution %s " %( str(userNo),user.username,len(InsObjs)))   
                                                """
                                                inscount=0
						for instObj in InsObjs:
								# if users has permission for all assessments in programme
								# check user has permission with instituion.
                                                                # if user has permission then assign assessment permission
                                                    if reportflag:
                                                                permInstObj=instObj 
                                                                # To generate Institution permission report
                                                                instPermData = []
                                                                boundaryStr = "%s --> %s --> %s" %(permInstObj.boundary, permInstObj.boundary.parent, permInstObj.boundary.parent.parent)
                                                                if inscount == 0:
                                                                       instPermData.append(user)
                                                                else:
                                                                                     instPermData.append(' ')
                                                                inscount=1
                                                                instPermData.append(permInstObj.name)
                                                                instPermData.append(boundaryStr)
                                                                instPermFile.writerow(instPermData)
                                         
						    if lenTrue==lenAsm or lenTrue== lenAsm-1: 							

                                                                        asmPermObj = UserAssessmentPermissions.objects.get_or_create(user=user, assessment = assessmentObj, instituion = instObj).defer('user','assessment')
                                                                       
                                                                        asmPermObj[0].access=1
                                                                        asmPermObj[0].save()  
                                                if reportflag:
							# To generate Assessment permission report.
							asmPermObjs = UserAssessmentPermissions.objects.filter(user=user, access = 1).defer('user','assessment')
							objCounter = 0
							for asmPermObj in asmPermObjs:
								asmPermData = []
								boundaryStr = "%s --> %s --> %s" %(asmPermObj.instituion.boundary, asmPermObj.instituion.boundary.parent, asmPermObj.instituion.boundary.parent.parent)
								if objCounter == 0:
									asmPermData.append(user)
								else:
									asmPermData.append(' ')
								asmPermData.append(asmPermObj.instituion.name)
								asmPermData.append(boundaryStr)
								asmPermData.append(asmPermObj.assessment)
								asmPermData.append(asmPermObj.assessment.programme)
								asmPermFile.writerow(asmPermData)
								objCounter += 1
                                               
                                                lastprocestime=datetime.datetime.now()-procestime
                                                procestime=datetime.datetime.now() 
                                                self.stdout.write("      Total time was taken for this user %s" %(str(lastprocestime)))
                                        self.stdout.write("\n Total time was taken for all the users %s \n" %(str(datetime.datetime.now()-starttime)))
				except : #except IOError:
					## If Arguments are not in proper order raises an command error
					raise CommandError('Pass First Parameter is FileName and Second Parameter is Assessment Id\n')
					
		except:#except IndexError:
			# If Arguments are not passed raises an command error
			raise CommandError('Pass FileName and Assessment Id\n')
