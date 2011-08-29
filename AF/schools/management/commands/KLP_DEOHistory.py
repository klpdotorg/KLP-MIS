from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from django.contrib.contenttypes.models import ContentType
from fullhistory.models import FullHistory
from django.db.models import Q 
from django.contrib.auth.models import User
import django, datetime, os, csv



class Command(BaseCommand):
	''' Command To generate Data Entry Operators History in csv format.'''
        def handle(self, *args, **options):
                try:
                	# read start date, end date and filename
                        startDate = args[0]
                        endDate = args[1]
                        fileName = args[2]
			contentList = ['boundary', 'institution', 'student', 'staff']
                        if fileName and startDate and endDate:  # If startdate, enddate and fileName passed procced else raise am error
                                try:
                                	strDate = startDate.split("/")
                                	enDate = endDate.split("/")
                                	# Get all active assessments for the active programme
    					assessments = Assessment.objects.select_related("programme").filter(programme__active=2, active=2).distinct().only("id", "name")
    					# get current working directory.
					cwd = os.getcwd()
					path = "%s/logFiles/" %(cwd)
                                        if not os.path.exists(path):
                                        	# if dir not exists creates directory with name logfiles in cwd.
                                                os.makedirs(path)
                                        # create csv file with the name passed.        
					genFile = "%s/%s.csv" %(path, fileName)
					historyFile = csv.writer(open(genFile, 'wb'))
					# Write header
					headerList = ['Sl.No', 'User', 'pre_boundary_created', 'pre_boundary_mod', 'pre_boundary_del', 'primary_boundary_created', 'primary_boundary_mod', 'primary_boundary_del', 'pre_sch_created', 'pre_sch_mod', 'pre_sch_del', 'primary_sch_created', 'primary_sch_mod', 'primary_sch_del', 'pre_stud_created', 'pre_stud_mod', 'pre_stud_del', 'primary_stud_created', 'primary_stud_mod', 'primary_stud_del', 'pre_teacher_created', 'pre_teacher_mod', 'pre_teacher_del', 'primary_teacher_created', 'primary_teacher_mod', 'primary_teacher_del']
					asmDict, asmList ={}, []					
					users = User.objects.filter(is_active=1).order_by("username").only("id", "username")  # Querying all active userid, usernames and sorting by username
					userIds = users.values_list("id", flat=True)   # getting only userids from queryset
					sDate = datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0]))
					eDate = datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0]))
					sTime = datetime.datetime(int(strDate[2]), int(strDate[1]), int(strDate[0]), 00, 00, 00)
					eTime = datetime.datetime(int(enDate[2]), int(enDate[1]), int(enDate[0]), 23, 59, 00)
					for assessment in assessments:
						# Querying created/modified answer id of the assessment in the date span
						answers = Answer.objects.filter(Q(user1__id__in=userIds) | Q(user2__id__in=userIds), lastModifiedDate__range=(sDate, eDate), question__assessment=assessment).values_list("id", flat=True).distinct()						
						if answers:   # if answers are created/modified in given date span adding header and passing answer ids to dictionary
							assessmentId = assessment.id
							asmList.append(assessmentId)
							# Adding header
							asmName = "%s-%s" %(assessment.programme.name, assessment.name)
							headerList.append(asmName+' Num Of correct Entries')
							headerList.append(asmName+' Num Of incorrect Entries')
							headerList.append(asmName+' Num Of verified Entries')
							headerList.append(asmName+' Num Of rectified Entries')
							nList = [i for i in answers]
							nList.append(0)
							asmDict[assessmentId] = nList
					historyFile.writerow(headerList)  # writting header to the file
					count = 0					
    					for user in User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'], is_active=1).order_by("username"):
						count +=1
						userId = user.id
				    		dataList = [count, user.username]
				    		
				    		rawQuerySet = Institution.objects.raw(""" SELECT "id","obj_id" FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = 't' """ %(userId))
				    		inst_list=[permObj.obj_id for permObj in rawQuerySet]		    		

						preSchList = Institution.objects.filter(id__in=inst_list, boundary__boundary_type__id=2).values_list("id", flat=True) #Querying for Pre schools
						primarySchList = Institution.objects.filter(id__in=inst_list, boundary__boundary_type__id=1).values_list("id", flat=True)  # Querying for primary schools
				    		for content in contentList:
				    			preList, primaryList= [0], [0]
				    			contObj = ContentType.objects.get(app_label='schools', name=content)  # get schools content object
				    			contId = contObj.id  # get schools content object id
				    			if content == 'boundary':  # Checking is content is boundary
				    				preBoundaryList, primaryBoundaryList = [], []
				    				BoundaryList = Institution.objects.filter(id__in=preSchList).values_list("boundary", flat=True).distinct()  # querying circle level boubndaries using pre schools
				    				preBoundaryList.extend(list(BoundaryList)) # appending circle level boubndaries to list
				    				
				    				BoundaryList = Boundary.objects.filter(id__in=preBoundaryList, boundary_type__id=2).values_list("parent", flat=True).distinct()  # querying project level boubndaries using pre schools
				    				preBoundaryList.extend(list(BoundaryList)) # appending project level boubndaries to list
				    				BoundaryList = Boundary.objects.filter(id__in=preBoundaryList, boundary_type__id=2).values_list("parent", flat=True).distinct()  # querying district level boubndaries using pre schools
				    				preBoundaryList.extend(list(BoundaryList )) # appending district level boubndaries to list				
				    				
				    				
				    				BoundaryList = Institution.objects.filter(id__in=primarySchList).values_list("boundary", flat=True).distinct()  # querying cluster level boubndaries using primary schools
				    				
				    				primaryBoundaryList.extend(list(BoundaryList))  # appending cluster level boubndaries to list
				    				BoundaryList = Boundary.objects.filter(id__in=primaryBoundaryList, boundary_type__id=2).values_list("parent", flat=True).distinct()  # querying block level boubndaries using primary schools
				    				primaryBoundaryList.extend(list(BoundaryList))  # appending block level boubndaries to list
				    				
				    				BoundaryList = Boundary.objects.filter(id__in=primaryBoundaryList, boundary_type__id=2).values_list("parent", flat=True).distinct()  # querying district level boubndaries using primary schools				
				    				primaryBoundaryList.extend(list(BoundaryList))  # appending district level boubndaries to list
				    				preList = ['%s' %i for i in preBoundaryList]
				    				primaryList = ['%s' %i for i in primaryBoundaryList]
				    			elif content == 'institution':   # Checking is content is institution
				    				preList = ['%s' %i for i in preSchList]
				    				primaryList = ['%s' %i for i in primarySchList]
				    			elif content == 'staff':         # Checking is content is staff
				    				preStaffList = Staff.objects.filter(institution__id__in=preSchList, institution__boundary__boundary_type__id=2).values_list("id", flat=True)  # querying for pre school staff
				    				primaryStaffList = Staff.objects.filter(institution__id__in=primarySchList, institution__boundary__boundary_type__id=1).values_list("id", flat=True)  # querying for primary school staff
				    				preList = ['%s' %i for i in preStaffList]
				    				primaryList = ['%s' %i for i in primaryStaffList]
				    			elif content == 'student':       # Checking is content is student
				    				preSGList = StudentGroup.objects.filter(institution__id__in=preSchList, institution__boundary__boundary_type__id=2).values_list("id", flat=True)  # querying for pre school student groups
				    				primarySGList =  StudentGroup.objects.filter(institution__id__in=primarySchList, institution__boundary__boundary_type__id=1).values_list("id", flat=True)  # querying for primary school student groups
				    				preStList = Student_StudentGroupRelation.objects.filter(student_group__id__in=preSGList).values_list("student",  flat=True)  # querying for pre school students
				    				primaryStList = Student_StudentGroupRelation.objects.filter(student_group__id__in=primarySGList).values_list("student",  flat=True)  # querying for primary school students
				    				preList = ['%s' %i for i in preStList]
				    				primaryList = ['%s' %i for i in primaryStList]
				    			
				    			
				    			preList.append(0)
				    			primaryList.append(0)
				    			
				    			
				    		        dataList.append(FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, content_type__id=contId, object_id__in=preList, action='C').count())  # querying for number of pre school/boundaries/staffs/students created by user in time span
				    			dataList.append(FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, content_type__id=contId, object_id__in=preList, action='U').exclude(_data__icontains='active').count())  # querying for number of pre schools/boundaries/staffs/students updated by user in time span
				    			
				    			dataList.append(FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, content_type__id=contId, object_id__in=preList, action='U', _data__icontains='active').count())  # querying for number of pre schools/boundaries/staffs/students deleted by user in time span
				    			
				    			dataList.append(FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, content_type__id=contId, object_id__in=primaryList, action='C').count())  # querying for number of primary school/boundaries/staffs/students created by user in time span
				    			dataList.append(FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, content_type__id=contId, object_id__in=primaryList, action='U').exclude(_data__icontains='active').count())  # querying for number of pre schools/boundaries/staffs/students updated by user in time span
				    			
				    			dataList.append(FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, content_type__id=contId, object_id__in=primaryList, action='U', _data__icontains='active').count())  # querying for number of pre schools/boundaries/staffs/students deleted by user in time span
				    			
				    			
				    		for asmId in asmList:
				    			# repeating assessments list
				    			answers =  asmDict[asmId]  # getting answers for the assessments
				    			if  answers:  # in answers created appending to report
								
				    				crEntriesData = FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, object_id__in=answers, action='C')  # querying for answers created by user
				    				crEntries = crEntriesData.count()  # getting correct entries count
				    				if crEntries == 0:
				    					# if correct entries count is 0 assigning incorrect entries to 0
				    					inCrEntries = 0
				    				else:
				    					# if correct entries is grater than 0 querying for incorrect entries
				    					crEntriesLis = list(crEntriesData.values_list("object_id", flat=True))
				    					inCrEntries = FullHistory.objects.filter((Q(_data__icontains='answer') | Q(_data__icontains='status')) & Q(_data__icontains='user2'), action_time__range=(sTime, eTime), object_id__in=crEntriesLis, action='U').exclude(request__user_pk=userId,).count()  
				    					
				    					crEntries = crEntries - inCrEntries   # subtracting incorrect entries from correct entries
				    				
				    				
				    				vEntries = FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, object_id__in=answers, action='U', _data__icontains='user2').exclude(Q(_data__icontains='id') | Q(_data__icontains='question') | Q(_data__icontains='student') ).count()   # querying for verified entries count
				    				
				    				rEntries = FullHistory.objects.filter((Q(_data__icontains='answer') | Q(_data__icontains='status')) & Q(_data__icontains='user2'), action_time__range=(sTime, eTime), request__user_pk=userId, object_id__in=answers, action='U').exclude(Q(_data__icontains='id') | Q(_data__icontains='question') | Q(_data__icontains='student') ).count()   # querying for rectified entries count
				    				
				    				
				    				vEntries = vEntries - rEntries   # subtracting rectified entries count from verified entries
				    				
				    				dataList.append(crEntries)
								dataList.append(inCrEntries)
								dataList.append(vEntries)
								dataList.append(rEntries)
				    		# Written data into file.
						historyFile.writerow(dataList)				    							    		
					print "%s.csv file has been created in %s/logFiles directory" %(fileName, cwd)
                                except IndexError:
                                	# if arguments are not proper raises an command error.
                                        raise CommandError('Date Should be in dd/mm/yyyy format.\n')
				except ValueError:
					# if arguments are not proper raises an command error.
					raise CommandError('Date Should be in dd/mm/yyyy format.\n')
                        else:
                        	# if arguments are not passed raises an command error.
                        	raise CommandError('Pass Startdate, end date and filename.\n') 

                except IndexError:
                	# if arguments are not passed raises an command error.
                        raise CommandError('Pass Startdate, end date and filename.\n') 

