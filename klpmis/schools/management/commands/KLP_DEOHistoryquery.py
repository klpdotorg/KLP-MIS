from django.core.management.base import BaseCommand, CommandError
from schools.models import *
from django.contrib.contenttypes.models import ContentType
from fullhistory.models import FullHistory
from django.db.models import Q 
from django.contrib.auth.models import User
import django, datetime, os, csv
import psycopg2
from klp.settings import *

class Command(BaseCommand):
	''' Command To generate Data Entry Operators History in csv format.'''
        def handle(self, *args, **options):
                if 1:
                	# read start date, end date and filename
                        start_date = args[0]
                        end_date = args[1]
                        fileName = args[2]
                        print datetime.datetime.now()
			contentList = ['institution', 'student', 'staff']
		    	d=DATABASES['default']
		    	datebase=d['NAME']
		    	user=d['USER']
		    	password=d['PASSWORD']
		    	connection = psycopg2.connect(database=datebase, user=user, password=password)
    			
                        if fileName and start_date and end_date:
                                try:
                                	strDate = start_date.split("/")
                                	enDate = end_date.split("/")
                                	
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
					contentdic={}
		    			for k in contentList:
		    			  contObj = ContentType.objects.get(app_label='schools', name=k)
		    			  contId = contObj.id
		    			  contentdic[k]=contId
		    			#, 'pre_boundary_created', 'pre_boundary_mod', 'pre_boundary_del', 'primary_boundary_created', 'primary_boundary_mod', 'primary_boundary_del',
					headerList = ['Sl.No', 'User', 'pre_sch_created', 'pre_sch_mod', 'pre_sch_del', 'primary_sch_created', 'primary_sch_mod', 'primary_sch_del', 'pre_stud_created', 'pre_stud_mod', 'pre_stud_del', 'primary_stud_created', 'primary_stud_mod', 'primary_stud_del', 'pre_teacher_created', 'pre_teacher_mod', 'pre_teacher_del', 'primary_teacher_created', 'primary_teacher_mod', 'primary_teacher_del']
					asmDict, asmList ={}, []
					users = User.objects.filter(is_active=1).order_by("username").only("id", "username")
					userIds = users.values_list("id", flat=True)
					sDate = datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0]))
					eDate = datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0]))
					sTime = datetime.datetime(int(strDate[2]), int(strDate[1]), int(strDate[0]), 00, 00, 00)
					eTime = datetime.datetime(int(enDate[2]), int(enDate[1]), int(enDate[0]), 23, 59, 00)
					FullhisoryAssessment="""select CAST(object_id AS INT) from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and content_type_id = 31""" % (sTime,eTime)
					print 'sTime=',sTime,'eTime=',eTime
    					assessments = Assessment.objects.raw("""select * from schools_assessment where programme_id in (select distinct id from schools_programme where active=2 )  and active=2 """ )  #and active=2
                                        cursor = connection.cursor()
                                        print """select CAST(object_id AS INT) from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and content_type_id = 31""" % (sTime,eTime)
					fullhistoryAnswers=cursor.execute("""select distinct CAST(object_id AS INT) from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and content_type_id = 31""" % (sTime,eTime))
                                        validAns=[c[0] for c in cursor.fetchall()]
                                        preboundarytypeId="""select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=2)"""
                                        cursor.execute(preboundarytypeId)
                                        preBoundaryList=[c[0] for c in cursor.fetchall()]
                                        primaryboundarytypeId="""select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=1)"""
                                        cursor.execute(primaryboundarytypeId)
                                        primaryBoundaryList=[c[0] for c in cursor.fetchall()]

                                        #validAns=validAns[:10]
					#cursor = connection.cursor()
                                        #print validAns
                                        #userids=cursor.execute("""select id  from auth_user where is_active is true""")
					user_ids=tuple(userIds) #User.objects.filter(is_active=1).values_list('id',flat=True)
                                        
					for assessment in assessments:
					    questions="""select id from schools_question where assessment_id= %s and active= 2""" % (assessment.id)
					    answerQuery=""" select distinct id from schools_answer  where (user1_id in %s or  user2_id in %s  ) and  question_id in (%s) and "last_modified_date" >'%s' and "last_modified_date" < '%s' and id in %s""" % (user_ids,user_ids,questions,sDate,eDate,tuple(validAns))
                                            print assessment.id
					    if 1: #assessment.id==130:
						#print 'anwser query',answerQuery
						cursor.execute(answerQuery)
						answersCur = cursor.fetchall() #Answer.objects.raw(answerQuery)
                                                answers=[c[0] for c in answersCur]
						if len(list(answers)):
						        print 'inner'
							assessmentId = assessment.id
							asmList.append(assessmentId)
							asmName = "%s-%s" %(assessment.programme.name, assessment.name)
							headerList.append(asmName+' Num Of correct Entries')
							headerList.append(asmName+' Num Of incorrect Entries')
							headerList.append(asmName+' Num Of verified Entries')
							headerList.append(asmName+' Num Of rectified Entries')
							
							asmDict[assessmentId] = answers #answerQuery
					print asmDict.keys(),'tttttttttttttttttttttttttttttt'		
					historyFile.writerow(headerList)
					count = 0
					
					#preboundarytypeId="""select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=2)"""
					#primaryboundarytypeId="""select id from schools_boundary where boundary_type_id in (select id from schools_boundary_type where id=1)"""				
					
    					for user in User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'], is_active=1).order_by("username"):    
    					   if user.id==112:
    					
    						klp_UserGroups = user.groups.all()
    						user_GroupsList = ['%s' %(str(usergroup.name)) for usergroup in klp_UserGroups]
						count +=1
						userId = user.id
				    		dataList = [count, user.username]
				    		IntrawQuerySet =""" SELECT obj_id FROM "public"."object_permissions_institution_perms" WHERE "user_id" = %s AND "Acess" = 1 """ %(userId)                   
				    	     
                                                preinstitutionQuery="""SELECT distinct id from schools_institution where id in ( %s ) and   boundary_id in %s and active=2  """ %(IntrawQuerySet,tuple(preBoundaryList))
                                                """cursor.execute(preinstitutionQuery)
                                                preInstLists=[c[0] for c in cursor.fetchall()]
                                                """
                                                primaryinstitutionQuery="""SELECT distinct id from schools_institution where id in ( %s ) and   boundary_id in %s and active=2 """ %(IntrawQuerySet,tuple(primaryBoundaryList ))
                                                """
                                                cursor.execute(primaryinstitutionQuery)
                                                primaryInstLists=[c[0] for c in cursor.fetchall()]
                                                """
				    		
					    		
						for content in contentdic:
				    			#preList, primaryList= [0], [0]
				    			
				    			contId = contentdic[content]
							fullhistoryQuery=""" in (select CAST(object_id AS INT) from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and content_type_id =%s )""" % (sTime,eTime,userId,contId)
				    			
				    			    		
					
			                                '''	
							preinstitutionQuery="""SELECT distinct id from schools_institution where id in ( %s ) and   boundary_id in %s and active=2  """ %(IntrawQuerySet,tuple(preBoundaryList))
							primaryinstitutionQuery="""SELECT distinct id from schools_institution where id in ( %s ) and   boundary_id in %s and active=2 """ %(IntrawQuerySet,tuple(primaryBoundaryList) )
                                                        
							
							preboundaryinstitutionQuery="""SELECT distinct boundary_id from schools_institution where id in ( %s ) and   boundary_id in (%s) and active=2 and  id %s""" %(IntrawQuerySet,preboundarytypeId,fullhistoryQuery )
						
							if content == 'boundary':
				    				preboundaryinstitutionQuery="""SELECT distinct boundary_id from schools_institution where id in ( %s ) and   boundary_id in (%s) and active=2 and id %s""" %(IntrawQuerySet,preboundarytypeId,fullhistoryQuery )
				    				
				    				#preBoundaryList.extend(list(BoundaryList))
				    				preboundaryinstitutionQuery1="""select parent_id from schools_boundary where id in(SELECT distinct boundary_id from schools_institution where id in ( %s ) and   boundary_id in (%s) and active=2 and id %s) and boundary_type_id in (%s) """ %(IntrawQuerySet,preboundarytypeId,fullhistoryQuery ,preboundaryinstitutionQuery)
				    				
				    				preboundaryinstitutionQuery2="""select parent_id from schools_boundary where id in(SELECT distinct boundary_id from schools_institution where id in ( %s ) and   boundary_id in (%s) and active=2 and id %s) and ( boundary_type_id in (%s) or boundary_type_id in (%s)) """ %(IntrawQuerySet,primaryboundarytypeId,fullhistoryQuery ,preboundaryinstitutionQuery,preboundaryinstitutionQuery1)
				    				
				    				preList=""" %s union %s union %s """ % (preboundaryinstitutionQuery,preboundaryinstitutionQuery1,preboundaryinstitutionQuery2)
				    				
				    				primaryboundaryinstitutionQuery="""SELECT distinct boundary_id from schools_institution where id in (%s) and   boundary_id in (%s) and active=2 and id %s""" %(IntrawQuerySet,primaryboundarytypeId,fullhistoryQuery )
				    				
				    				primaryboundaryinstitutionQuery1="""select parent_id from schools_boundary where id in(SELECT distinct boundary_id from schools_institution where id in ( %s ) and   boundary_id in (%s) and active=2 and in %s) and boundary_type_id in (%s) """ %(IntrawQuerySet,primaryboundarytypeId,fullhistoryQuery ,primaryboundaryinstitutionQuery)
				    				
				    				primaryboundaryinstitutionQuery2="""select parent_id from schools_boundary where id in(SELECT distinct boundary_id from schools_institution where id in ( %s ) and   boundary_id in (%s) and active=2 and in %s) and ( boundary_type_id in (%s) or boundary_type_id in (%s)) """ %(IntrawQuerySet,primaryboundarytypeId,fullhistoryQuery ,primaryboundaryinstitutionQuery,primaryboundaryinstitutionQuery1)
				    				
				    				primaryList=""" %s union %s union %s """ % (primaryboundaryinstitutionQuery,primaryboundaryinstitutionQuery1,primaryboundaryinstitutionQuery2)
                                                        '''
				    			if content == 'institution':
				    				preList = """%s and id %s """ % (preinstitutionQuery ,fullhistoryQuery )
                                                                cursor.execute(preList) 
                                                                preListId=tuple([c[0] for c in cursor.fetchall()])
				    				primaryList = """%s and id %s """ % (primaryinstitutionQuery,fullhistoryQuery)
                                                                primaryListId=tuple([c[0] for c in cursor.fetchall()])
                                                                #preList=preListId
                                                                #primaryList=primaryListId
                                                                #primaryListId,preListId=[],[]
				    			elif content=='staff':
				    				
				    				preList="""select distinct id from schools_staff where institution_id in %s and id %s """ %(preListId,fullhistoryQuery )
				    				
				    				primaryList="""select distinct id from schools_staff where institution_id in %s and id %s """ %(primaryListId,fullhistoryQuery )
				    			elif content == 'student':
				    			           preList = """select distinct student_id  from schools_Student_StudentGroupRelation where student_group_id in (select id from schools_studentgroup where institution_id in  %s ) and student_id %s  """ % (preListId,fullhistoryQuery )
				    				   primaryList = """select distinct student_id from schools_Student_StudentGroupRelation where student_group_id in (select id from schools_studentgroup where institution_id in  %s  ) and student_id %s """ % (primaryListId,fullhistoryQuery)
				    			if content=='institution' :
                                                                  loopList=[preListId,primaryListId]
                                                        else:
                                                          LoopList=[preList ,primaryList]
				    			for listobj in loopList:
				    				
	                                                	if  ('Data Entry Executive' in user_GroupsList and content in ['institution', 'staff', 'studentgroup', 'student']) or ('Data Entry Operator' in user_GroupsList and content in ['student']): 
                                                                        if content!='institution':
	                                                		   createdhistoryraw="""select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and content_type_id =%s and CAST(object_id AS INT) in (%s) and action='C' """ % (sTime,eTime,userId,contId,listobj)
				    			
	                                                  		   updatedhistoryraw="""select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and content_type_id =%s and CAST(object_id AS INT) in (%s) and action='U'""" % (sTime,eTime,userId,contId,listobj)
                                                                        else:
                                                                                createdhistoryraw="""select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and content_type_id =%s and CAST(object_id AS INT) in %s and action='C' """ % (sTime,eTime,userId,contId,listobj)
                                                        
                                                                                updatedhistoryraw="""select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and content_type_id =%s and CAST(object_id AS INT) in %s and action='U'""" % (sTime,eTime,userId,contId,listobj)
			                                        	activeupdated=updatedhistoryraw+""" and data ilike '%%active%%'"""
			                                        	notactiveupdated=updatedhistoryraw+""" and data not ilike '%%active%%'"""
			                                        	
			                                       
	                                                
					                                cursor.execute(createdhistoryraw)
					                                row= cursor.fetchone()
						    		        dataList.append(row and row[0] or 0 )
						    		        
						    		        cursor.execute(notactiveupdated)
						    		        row= cursor.fetchone()
						    		        dataList.append(row and row[0] or 0)
						    		       
						    		        cursor.execute(activeupdated)
						    		        row= cursor.fetchone()
						    			dataList.append(row and row[0] or 0)
						    		
					    			else:
					    		    		dataList=dataList+[0, 0, 0]
					    		
					    	loopList,preList,primaryList=[],[],[]	
				    		print 'userId***************',userId,dataList
						for asmId in asmList:
                                                 print asmId,'ASSSSSSSSSSSSSSSSSSSSSS'
                                                 if 1:
				    			answers =  tuple(asmDict[asmId])
	                                                #print answers,sTime,eTime
	                                                
							crQuery="""select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s )  and CAST(object_id AS INT)  in %s and action='C'""" % (sTime,eTime,userId,answers)
							#print 'ansswers',asmId ,crQuery
							
				    			#print 'crQuery ',crQuery
							
							#print crQuery
							cursor.execute(crQuery)
							row=cursor.fetchone()	
			    				crEntriesData = row and row[0] or 0
			    				crEntries = crEntriesData
                                                        #print 'crEntris'
			    				if crEntries == 0:
			    					inCrEntries = 0
			    				else:
			    				
			    					inCrQuery="""select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s )  and CAST(object_id AS INT)  in %s and action='U' and (data like '%%anwsers%%' or data like '%%status%%' or data like '%%user2%%') and request_id  not in (select id from fullhistory_request where user_pk =%s )""" % (sTime,eTime,userId,answers,userId)	
			    					
			    					#print 'incRquery',inCrQuery
			    					
			    					cursor.execute(inCrQuery)
			    					row=cursor.fetchone()	
			    					inCrEntries = row and row[0] or 0
			    					
			    					crEntries = crEntries - inCrEntries
			    				
			    				vQuery="""select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and CAST(object_id AS INT)  in %s and action='U'  and request_id  not in (select id from fullhistory_request where user_pk =%s )  and (data not like '%%id%%' or data not like '%%question%%' or data not like '%%student%%')""" % (sTime,eTime,userId,answers,userId)	
			    				
			    				#print 'vQuery',vQuery
			    				cursor.execute(vQuery)
			    				row=cursor.fetchone()
			    				vEntries = row and row[0] or 0  #len(list(FullHistory.objects.raw(vQuery)))
			    				
			    				rQuery="""select count(id) as count from fullhistory_fullhistory where action_time > '%s' and action_time < '%s' and request_id  in (select id from fullhistory_request where user_pk =%s ) and CAST(object_id AS INT)  in %s and action='U' and (data like '%%anwsers%%' or data like '%%status%%' or data like '%%user2%%') and request_id  not in (select id from fullhistory_request where user_pk =%s )  and (data not like '%%id%%' or data not like '%%question%%' or data not like '%%student%%')""" % (sTime,eTime,userId,answers,userId)
			    				
			    				print 'rQuery',rQuery
			    				cursor.execute(rQuery)
			    				row=cursor.fetchone()		
			    				rEntries = row and row[0] or 0 # #len(list(FullHistory.objects.raw(rQuery)))
			    				
			    				
			    				vEntries = vEntries - rEntries
			    				#print userId,crEntries,inCrEntries,vEntries,rEntries
			    				dataList.append(crEntries)
							dataList.append(inCrEntries)
							dataList.append(vEntries)
							dataList.append(rEntries)		    							  
								
						print dataList 
						historyFile = csv.writer(open(genFile, 'a'))	
						historyFile.writerow(dataList)	 
							
					print "%s.csv file has been created in %s/logFiles directory" %(fileName, cwd)
					print datetime.datetime.now()
				
                                except IndexError:
                                	# if arguments are not proper raises an command error.
                                        raise CommandError('Date Should be in dd/mm/yyyy format.\n')
				except ValueError:
					# if arguments are not proper raises an command error.
					raise CommandError('Date Should be in dd/mm/yyyy format.\n')
				except :
				       pass
				finally:
				       cursor.close()	
                        else:
                        	# if arguments are not passed raises an command error.
                        	raise CommandError('Pass Startdate, end date and filename.\n') 

                else : #:
                	# if arguments are not passed raises an command error.
                        raise CommandError('Pass Startdate, end date and filename.\n') 

