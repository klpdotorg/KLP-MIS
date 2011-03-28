from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from django.contrib.contenttypes.models import ContentType
from fullhistory.models import FullHistory
import django, datetime, os, csv

class Command(BaseCommand):
        #args = '<inst_id inst_id ...>'
        #help = 'Students Promoting to Next Year'

        def handle(self, *args, **options):
                try:
                        startDate = args[0]
                        endDate = args[1]
                        fileName = args[2]
			contentList = ['institution', 'student', 'staff']
                        if fileName and startDate and endDate:
                                try:
                                	strDate = startDate.split("/")
                                	enDate = endDate.split("/")
                                        deDict, respDict = {},{}
    					activePrgs = Programme.objects.filter(active=2).values_list("id", flat=True)
    					assessments = Assessment.objects.filter(programme__id__in=activePrgs, active=2).distinct()
    					respDict['assessments'] = assessments
					cwd = os.getcwd()
					path = "%s/logFiles/" %(cwd)
                                        if not os.path.exists(path):
                                                os.makedirs(path)
					genFile = "%s/%s.csv" %(path, fileName)
					historyFile = csv.writer(open(genFile, 'wb'))
					headerList = ['Sl.No', 'User', 'sch_created', 'sch_mod', 'stud_created', 'stud_mod', 'teacher_created', 'teacher_mod']
					for assessment in assessments:
						asmName = assessment.name
						headerList.append(asmName)
						headerList.append(asmName+'_DE')
					historyFile.writerow(headerList)
					count = 0
    					for user in User.objects.filter(is_active=1):
						count +=1
				    		dataList = [count, user.username]
						actDict = {}
				    		for content in contentList:
				    			contObj = ContentType.objects.get(app_label='schools', name=content)
				    		        dataList.append(len(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, content_type__id=contObj.id, action='C')))
				    			dataList.append(len(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, content_type__id=contObj.id, action='U')))
				    		for assessment in assessments:
				    			questions = Question.objects.filter(assessment = assessment,active=2).values_list("id", flat=True).distinct()
				    			answers = Answer.objects.filter(question__id__in=questions).values_list("id", flat=True).distinct()
				    			if len(answers) == 0:
								dataList.append(0)
								dataList.append(0)
				    			else:	
				    				nList = [i for i in answers]
				    				dataList.append(len(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, object_id__in=nList, action='C')))
				    			 	dataList.append(len(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, object_id__in=nList, action='U', _data__icontains='answer')))
						historyFile.writerow(dataList)				    							    		
					#historyFile.close()
					print "%s.csv file has been created in %s/logFiles directory" %(fileName, cwd)
                                except IndexError:
                                        raise CommandError('Date Should be in dd/mm/yyyy format.\n')
				except ValueError:
					raise CommandError('Date Should be in dd/mm/yyyy format.\n')
                        else:
                        	raise CommandError('Pass Startdate, end date and filename.\n') 

                except IndexError:
                        raise CommandError('Pass Startdate, end date and filename.\n') 

