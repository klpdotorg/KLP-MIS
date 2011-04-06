from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from django.contrib.contenttypes.models import ContentType
from fullhistory.models import FullHistory
import django, datetime, os, csv

class Command(BaseCommand):
	''' Command To generate Data Entry Operators History in csv format.'''
        def handle(self, *args, **options):
                try:
                	# read start date, end date and filename
                        startDate = args[0]
                        endDate = args[1]
                        fileName = args[2]
			contentList = ['institution', 'student', 'staff']
                        if fileName and startDate and endDate:
                                try:
                                	strDate = startDate.split("/")
                                	enDate = endDate.split("/")
    					activePrgs = Programme.objects.filter(active=2).values_list("id", flat=True)
    					assessments = Assessment.objects.filter(programme__id__in=activePrgs, active=2).distinct().only("id", "name")
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
					headerList = ['Sl.No', 'User', 'sch_created', 'sch_mod', 'stud_created', 'stud_mod', 'teacher_created', 'teacher_mod']
					for assessment in assessments:
						asmName = assessment.name
						headerList.append(asmName+' Num Of correct Entries')
						headerList.append(asmName+' Num Of incorrect Entries')
						headerList.append(asmName+' Num Of verified Entries')
						headerList.append(asmName+' Num Of rectified Entries')
					historyFile.writerow(headerList)
					count = 0
    					for user in User.objects.filter(is_active=1).order_by("username").only("id", "username"):
						count +=1
				    		dataList = [count, user.username]
						# get the content objects(instituion, staff, student)
				    		for content in contentList:
				    			contObj = ContentType.objects.get(app_label='schools', name=content)
				    			# get all instituion/staff/student creates/Edited by user.
				    		        dataList.append(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, content_type__id=contObj.id, action='C').count())
				    			dataList.append(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, content_type__id=contObj.id, action='U').count())
				    			
				    		for assessment in assessments:
				    			answers = Answer.objects.filter(question__assessment=assessment).values_list("id", flat=True).distinct()
				    			if len(answers) == 0:
								dataList.append(0)
								dataList.append(0)
								dataList.append(0)
								dataList.append(0)
				    			else:	
				    				nList = [i for i in answers]
				    				crEntries = FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, object_id__in=nList, action='C').count()
				    				if crEntries == 0:
				    					inCrEntries = 0
				    				else:
				    					inCrEntries = FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), object_id__in=nList, action='U', _data__icontains='answer').count()
				    					crEntries = crEntries - inCrEntries
				    				
				    				
				    				vEntries = FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, object_id__in=nList, action='U').count()
				    				
				    				rEntries = FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, object_id__in=nList, action='U', _data__icontains='answer').count()
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

