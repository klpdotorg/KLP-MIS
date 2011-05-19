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
                        if fileName and startDate and endDate:
                                try:
                                	strDate = startDate.split("/")
                                	enDate = endDate.split("/")
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
					headerList = ['Sl.No', 'User', 'boundary_created', 'boundary_mod', 'sch_created', 'sch_mod', 'stud_created', 'stud_mod', 'teacher_created', 'teacher_mod']
					asmDict, asmList ={}, []
					users = User.objects.filter(is_active=1).order_by("username").only("id", "username")
					userIds = users.values_list("id", flat=True)
					sDate = datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0]))
					eDate = datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0]))
					sTime = datetime.datetime(int(strDate[2]), int(strDate[1]), int(strDate[0]), 00, 00, 00)
					eTime = datetime.datetime(int(enDate[2]), int(enDate[1]), int(enDate[0]), 23, 59, 00)
					for assessment in assessments:
						
						answers = Answer.objects.filter(Q(user1__id__in=userIds) | Q(user2__id__in=userIds), lastModifiedDate__range=(sDate, eDate), question__assessment=assessment).values_list("id", flat=True).distinct()
						if answers:
							assessmentId = assessment.id
							asmList.append(assessmentId)
							asmName = "%s-%s" %(assessment.programme.name, assessment.name)
							headerList.append(asmName+' Num Of correct Entries')
							headerList.append(asmName+' Num Of incorrect Entries')
							headerList.append(asmName+' Num Of verified Entries')
							headerList.append(asmName+' Num Of rectified Entries')
							nList = [i for i in answers]
							nList.append(0)
							asmDict[assessmentId] = nList
					historyFile.writerow(headerList)
					count = 0
					
    					for user in User.objects.filter(is_active=1).order_by("username").only("id", "username"):
						count +=1
						userId = user.id
				    		dataList = [count, user.username]
						# get the content objects(instituion, staff, student)
				    		for content in contentList:
				    			contObj = ContentType.objects.get(app_label='schools', name=content)
				    			# get all boundary/instituion/staff/student creates/Edited by user.
				    		        dataList.append(FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, content_type__id=contObj.id, action='C').count())
				    			dataList.append(FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, content_type__id=contObj.id, action='U').count())
				    			
				    		for asmId in asmList:
				    			answers =  asmDict[asmId]
				    			if  answers:
								
				    				crEntries = FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, object_id__in=answers, action='C').count()
				    				if crEntries == 0:
				    					inCrEntries = 0
				    				else:
				    					inCrEntries = FullHistory.objects.filter((Q(_data__icontains='answer') | Q(_data__icontains='status')) & Q(_data__icontains='user2'), action_time__range=(sTime, eTime), object_id__in=answers, action='U').exclude(request__user_pk=userId,).count()
				    					
				    					crEntries = crEntries - inCrEntries
				    				
				    				
				    				vEntries = FullHistory.objects.filter(action_time__range=(sTime, eTime), request__user_pk=userId, object_id__in=answers, action='U', _data__icontains='user2').count()
				    				
				    				rEntries = FullHistory.objects.filter((Q(_data__icontains='answer') | Q(_data__icontains='status')) & Q(_data__icontains='user2'), action_time__range=(sTime, eTime), request__user_pk=userId, object_id__in=answers, action='U').count() 
				    				
				    				
				    				vEntries = vEntries - rEntries
				    				
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

