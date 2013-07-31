"""

StudentGroupApi is used 
1) To view Individual StudentGroup details.
2) To create new StudentGroup
3) To update existing StudentGroup
4) To view assessment entry screen or grid to enter answers data.
"""
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry
from django.contrib.contenttypes.models import ContentType

from schools.receivers import KLP_user_Perm
from django.forms.models import modelformset_factory
from klpmis.settings import NUM_OF_FLEXI_ANSWER_FORM_RECORDS

class KLP_StudentGroup(Collection):
    def get_entry(self, studentgroup_id):    
    	# Query For Selected Student Group based on studentgroup_id    
        StudentGroups = StudentGroup.objects.get(id=studentgroup_id)          
        return ChoiceEntry(self,StudentGroups )

def KLP_StudentGroup_Create(request, referKey):
	""" To Create New StudentGroup boundary/(?P<bounday>\d+)/schools/(?P<school>\d+)/class/creator/"""
	#Checking user Permissions for SG add
        KLP_user_Perm(request.user, "StudentGroup", "Add")
	buttonType = request.POST.get('form-buttonType')
	instObj = Institution.objects.get(id = referKey)
	group_typ = request.GET.get("group_typ") or request.POST.get("group_typ")
        #before StudentGroup.objects.all()
        KLP_Create_StudentGroup = KLP_StudentGroup(queryset = StudentGroup.objects.filter(pk=0), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'studentgroup', extra_context={'buttonType':buttonType, 'ParentKey':referKey, 'group_typ':group_typ, 'sch_typ':instObj.boundary.boundary_category.boundary_category}), receiver = XMLReceiver(),)
        response = KLP_Create_StudentGroup.responder.create_form(request,form_class=StudentGroup_Form)
        return HttpResponse(response)
	
	
def KLP_StudentGroup_View(request, studentgroup_id):
	""" To View Selected StudentGroup studentsroup/(?P<studentsroup_id>\d+)/view/?$"""
	reqlist= request.GET.items()
	itemlist=[str(k[0]) for k in reqlist]
	if 'count' in itemlist:
		count = request.GET['count']
	else:
		count = '0'
	kwrg = {'is_entry':True}
	studentgroup = StudentGroup.objects.get(id=studentgroup_id)
	url = '/studentgroup/'+studentgroup_id+'/view/'
	school = Institution.objects.get(id = studentgroup.institution.id)
	studgrpParent = school
	# Get All centers under Institution
	studentGroups = StudentGroup.objects.filter(institution__id=studgrpParent.id,group_type="Center", active=2)
	# Get Total Number of students 
	Norecords = Student_StudentGroupRelation.objects.filter(student_group__id = studentgroup_id,academic=current_academic, active=2).count()
	# Query Child onjects
	child_list = Student_StudentGroupRelation.objects.filter(student_group__id = studentgroup_id, academic=current_academic, active=2, student__active=2).values_list('student__child', flat=True)
	
	students = Child.objects.filter(id__in=child_list).extra(select={'lower_firstname':'lower(trim("first_name"))', 'lower_midname':'lower(trim("middle_name"))', 'lower_lastname':'lower(trim("last_name"))' }).order_by('lower_firstname', 'lower_midname', 'lower_lastname')
	resp=Collection(students, permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'students',paginate_by = 20,extra_context={'studgrpParent':studgrpParent,'studentgroup':studentgroup,'url':url, 'students':students,'Norecords':Norecords, 'studentGroups':studentGroups,'count':count}),)
        return HttpResponse(resp(request))

def KLP_StudentGroup_Update(request, studentgroup_id):
	""" To update Selected School school/(?P<school_id>\d+)/update/"""
	#Checking user Permissions for SG update
        KLP_user_Perm(request.user, "StudentGroup", "Update")
	buttonType = request.POST.get('form-buttonType')
	ParentKey = request.POST.get('form-0-institution')
	group_typ = request.GET.get("group_typ") or request.POST.get("group_typ")
	sgObj = StudentGroup.objects.get(pk=studentgroup_id)
	sch_typ = request.GET.get("sch_typ") or sgObj.institution.boundary.boundary_category
        #before StudentGroup.objects.all()
	KLP_Edit_StudentGroup =KLP_StudentGroup(queryset = StudentGroup.objects.filter(pk=studentgroup_id), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'studentgroup', extra_context={'buttonType':buttonType,'ParentKey':ParentKey, 'group_typ':group_typ, 'sch_typ':sch_typ}), receiver = XMLReceiver(),)
	response = KLP_Edit_StudentGroup.responder.update_form(request, pk=studentgroup_id, form_class=StudentGroup_Form)
	return HttpResponse(response)	

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def KLP_StudentGroup_Answer_Entry(request, studentgroup_id, programme_id, assessment_id):

	""" To Show Answer Entry Form studentgroup/(?P<studentgroup_id>\d+)/programme/(?P<programme_id>\d+)/assessment/(?P<assessment_id>\d+)/view/"""
	""" This Method is used for to generate student answers grid to enter data/answers for the assessment questions """
	user = request.user  #get logged in user
	url = "/studentgroup/%s/programme/%s/assessment/%s/view/" %(studentgroup_id, programme_id, assessment_id)
	ordercounter=NUM_OF_FLEXI_ANSWER_FORM_RECORDS
	# Query Childs based on studentgroup relation
        AssObj=Assessment.objects.get(id=assessment_id)
        if AssObj.typ ==3:
        	students = Student_StudentGroupRelation.objects.select_related("student").filter(student_group__id = studentgroup_id,academic=current_academic, active=2).values_list('student__child', flat=True).distinct()
	        grupObj = StudentGroup.objects.filter(pk = studentgroup_id).only("group_type")[0].group_type
         	childs_list = Child.objects.filter(id__in=students).extra(select={'lower_firstname':'lower(trim("first_name"))' }).order_by('lower_firstname').defer("mt")
        elif AssObj.typ ==2:
                                         childs_list=StudentGroup.objects.filter(pk = studentgroup_id)
                                         grupObj =childs_list.only("group_type")[0].group_type
        else:
                                  childs_list=Institution.objects.filter(id=studentgroup_id)
                                  grupObj=''
        question_list = Question.objects.filter(assessment__id=assessment_id, active=2).defer("assessment").distinct()
       
        ansObjs=Answer.objects.filter(id=0)             
        studIdList, qNamesList, qIdList, chList, rDict, childDict, counter=[], [], [], [], {}, {}, 0
	paginator = Paginator(childs_list, 20)
	
	page = request.GET.get('page')  #get page to show result
	try:
		page = int(page)        # If page is there convert to inr 
	except (ValueError, TypeError):
		page = 1                # else default page is 1
	try:
		pagchilds_list = paginator.page(page)
	except (EmptyPage, InvalidPage):
		# If page is out of range (e.g. 9999), deliver last page of results.
		pagchilds_list = paginator.page(paginator.num_pages)
	objList=pagchilds_list.object_list
	studIdListprifix=[]
	for index,child in enumerate(objList):
		chDic={}
			
		chId = child.id
		chList.append(chId)
		# Query for active student using child object
             	if AssObj.typ ==3:
                                     student = Student.objects.filter(child=child, active=2).defer("child")
	                             studId = student[0].id
                                     # get Child and student information to show in grid.
              	                     if child.dob:
                                			dOfB = child.dob.strftime("%d-%m-%Y")
		                     else:
                          			dOfB = ''
		                     chDic = {'studId':studId, 'Gender':child.gender, 'dob':dOfB, 'first_name':child.first_name, 'last_name':child.last_name}
                                     # get relations
			             try:			
                                   			relObj = Relations.objects.filter(child=child, relation_type="Father").only("first_name")
                                        		chDic['fName'] = relObj[0].first_name
                                     except:
                               			chDic['fName'] = ''
		
                                     try:
                       			relObj = Relations.objects.filter(child=child, relation_type="Mother").only("first_name")
		                 	chDic['mName'] = relObj[0].first_name
                                     except:
                      			chDic['mName'] = ''
                                     #studIdListprifix.append(int(studId)+'_'+str(index))			
                                     studIdList.append(int(studId))
		                     childDict[chId] = chDic
                elif AssObj.typ==2:
                                                           chDic={'instId':studentgroup_id,'name':child.name+" "+child.section}
                                                           studIdList.append(int(studentgroup_id))
                                                           #studIdListprifix.append(str(studentgroup_id)+'_'+str(index))
                                                           childDict[chId] = chDic
                else:
                                           chDic={'instId':studentgroup_id,'name':child.name}
                                           studIdList.append(int(studentgroup_id))
                                           #studIdListprifix.append(str(studentgroup_id)+'_'+str(index))
                                           childDict[chId] = chDic
	rDict, ansStudList={}, []
	counter = counter +1 
	previouslenth=len(studIdList)


        if AssObj.flexi_assessment: 
            ansflexObj = list(set(Answer.objects.filter(question__in=question_list, object_id__in = studIdList).distinct().order_by('id').values_list('flexi_data',flat=True)))
            ansflexObj.sort()
        else:
            ansflexObj = Answer.objects.filter(question__in=question_list, object_id__in = studIdList).order_by('id').values_list('flexi_data',flat=True)
        if ansflexObj:
            ansflexObj = list(ansflexObj)

        if len(ansflexObj) >= ordercounter:
            ordercounter = 20
        print ansflexObj,'FFFFFFFFFFFFFFFFFFFFL' 
	qIdList=question_list.values_list('id',flat=True).distinct()
	qNamesList=question_list.values_list('name',flat=True).distinct()
	lookupfields=''
	QuestionDataDic={}
	for qindex,ques in enumerate(question_list):
		#qNamesList.append(ques.name)
		# get Question Information
		qId = ques.id
		#qIdList.append(qId)
		dataDict={'qId':qId, 'qOrder':ques.order}
		qType = ques.question_type
		dataDict['qType'] = qType		
		Adouble_entry=ques.assessment.double_entry
		if qType == 2:
			# if quetion type is 2(marks) get grades to do validation while data entry
			ansIn =  ques.grade
			dataDict['ansIn'] = ansIn
		else:
			# else get minmum and maximum score to do validation while data entry
			dataDict['scMin'] = ques.score_min
			dataDict['scMax'] = ques.score_max
		QuestionDataDic[qId]=dataDict

	if not AssObj.flexi_assessment :
		ansflexObj=range(len(chList))
	else:
                lenansflexObj=len(ansflexObj)
                if AssObj.primary_field_type==4:
                        lookupfields=Assessment_Lookup.objects.filter(assessment=AssObj).order_by('rank','name')
                        ordercounter=len(lookupfields)
                        #lenansflexObj=ordercounter
                        lookupfieldsnames=dict(lookupfields.values_list('id','name') )
		chList=chList*ordercounter
		#lenansflexObj=len(ansflexObj)
		studentId=chList[0]

	
	for indi,flexidata in enumerate(ansflexObj):
		ind=indi+1
		for qindex,ques in enumerate(question_list):
			#qNamesList.append(ques.name)
			# get Question Information
			qId = ques.id
			#qIdList.append(qId)
			dataDict=QuestionDataDic[qId]
                        qType=dataDict.get('qType')
			qDict={}	
			# Query For Answers based on question id and studens
			if not AssObj.flexi_assessment :
				studentId=chList[indi]
				flexidata=''
                                if AssObj.typ==3:
                                        studentId=studIdList[indi]
				ansObjs=ansObj = Answer.objects.select_related("user1").filter(question__id=qId, object_id = studentId)
			else:
				ansObjs=ansObj = Answer.objects.select_related("user1").filter(question__id=qId, object_id__in = studIdList,flexi_data=flexidata)				
			ansList = ansObj.defer("question").values()
       
			flexi_data=''
			ansStudListprefix=[]				
			if ansObj:
				for index,ansObj in enumerate(ansList):
					
					# If answers is there get answer Information
					ansDict=dict(dataDict)
					dEntry = ansObj['double_entry']
		
					firstUser = ansObj['user1_id']
					studentId = ansObj['object_id']
					ansStudList.append(studentId)
									
					if dEntry == 2:
						# if dEntry is 2 (doubleentry is finished) then dont show input box
						ansDict['iBox'] = False
					else:
						# else show input box
						ansDict['iBox'] = True
					if dEntry == 2 and Adouble_entry ==False and firstUser==user.id:
							# if dEntry is 2 and assesment double entry is false and first user is matched with logged in user then input box will show (refer ticket 322)x
							ansDict['iBox'] =True
	                                if AssObj.primary_field_type==4 and AssObj.flexi_assessment:
        
                                                 ansDict['lookupname']=lookupfieldsnames[int(ansObj['flexi_data'])]
                                        if AssObj.flexi_assessment and AssObj.primary_field_type !=4:
                                                 ansDict['lookupname']=ansObj['flexi_data']
					status = ansObj['status']
					if status == -99999:
						# if answer status is -99999(absent) then show answer value as 'AB'.
						ansVal = 'AB'
					elif status == -1:
							# if answer status is -1(unknown) then show answer value as 'UK'.
							ansVal = 'UK'
					elif qType == 2:
							# if question type is 2(grade) then show answer grade
							ansVal = ansObj['answer_grade']
					else:
							# else show answer score
							ansVal = ansObj['answer_score']
					ansDict['ansVal']=ansVal
					ansDict['flexi_data']=ansObj['flexi_data']
					if ansObj['flexi_data']:
						flexi_data=ansObj['flexi_data']
					ansDict['ansId']=ansObj['id']					
					ansDict['shVal'] = False	  
					if firstUser != user.id and dEntry ==1:
						# if dEntry is 1, (first entry finished doubleentry is not finished) and logged in user is not match with first user who enter data, then make dE attribute true to do validation while doubleentry
						ansDict['dE'] = True
					elif (firstUser == user.id and dEntry ==1) or (dEntry == 2 and Adouble_entry ==False and firstUser==user.id):
						# if dEntry is 1, (first entry finished doubleentry is not finished) and logged in user is match with first user who enter data, then make shVal attribute true to show answer value in input box.
						ansDict['shVal'] = True
					
					qDict[str(studentId)+'_'+str(ind)] = ansDict
			
	
			else:
						ansDict=dict(dataDict)
						ansDict['iBox'] = True
						ansDict['ansVal'] = ''
						ansDict['flexi_data'] = flexidata

						qDict[str(studentId)+'_'+str(ind)] = ansDict
			studIdListprifix.append(str(studentId)+'_'+str(ind))
						
			
			rDict[str(qId)+'_'+str(studentId)+'_'+str(ind)] = ansDict
	
	
	
	
	
	if AssObj.flexi_assessment :
                if  AssObj.primary_field_type!=4 and lenansflexObj < ordercounter :
                       rangeVar=(ordercounter-lenansflexObj)+1
                elif AssObj.primary_field_type ==4 :
                        rangeVar=1

		
		studIdList=studIdList*ordercounter
		for k in range(1,(ordercounter-lenansflexObj)+1):
			qDict={}
			for qindex,ques in enumerate(question_list):
				qId=ques.id
				dataDict=QuestionDataDic[qId]
				ansDict=dict(dataDict)
				ansDict['iBox'] = True
				ansDict['ansVal'] = ''
				ansDict['flexi_data'] = ''							
				qDict[str(studentId)+'_'+str(k+lenansflexObj)] = ansDict
				studIdListprifix.append(str(studentId)+'_'+str(k+lenansflexObj))
						
			
				rDict[str(qId)+'_'+str(studentId)+'_'+str(k+lenansflexObj)] = ansDict							
	noAnsList = list(set(studIdList).difference(set(ansStudList)))
	noAnsListprefix =list(set(studIdListprifix))
	noAnsListprefix.sort()
	#lookupfields=''
	#if AssObj.primary_field_type==4 :
	#	lookupfields=Assessment_Lookup.objects.filter(assessment=AssObj)
        ResourceForm = modelformset_factory(Answer,form=Answer_Form)
        form = ResourceForm(queryset=ansObjs.model.objects.none())		
	val=Collection(childs_list, permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'prgtemplates', template_object_name = 'childs', paginate_by=20, extra_context={'filter_id':programme_id, 'assessment_id':assessment_id, 'user':user, 'studentgroup_id':studentgroup_id, 'question_list':question_list,  'group_typ':grupObj, 'url':url, 'studIdList':studIdList ,  'qNamesList':qNamesList, 'chList':chList, 'childDict':childDict, 'rDict':rDict, 'qIdList':qIdList,'AssObj':AssObj,'loguser':request.user.id, 'lookupfields':lookupfields,'studIdListprifix':noAnsListprefix,'ordercounter':ordercounter,'formmanage':form.management_form}), entry_class = ChoiceEntry)
	return HttpResponse(val(request))
	

def MapStudents(request,id):
	""" To Map Students With Centers"""
	student_id = request.POST.getlist('students')
	count = 0
	if request.POST['StdgrpCtr'] == 'None':
		studentgroup_id = ''
	else:
		studentgroup_id = request.POST['StdgrpCtr']
	if student_id and studentgroup_id:
		# if Student and Student Group Id
		studentgroup =  StudentGroup.objects.get(pk = studentgroup_id)
		school =  Institution.objects.get(pk = request.POST['school'])
		academic =  Academic_Year.objects.get(pk = current_academic().id) 
		# Create Relation between Student and center
		for student in student_id:
			childObj = Child.objects.get(pk = student)
			student = Student.objects.get(child = childObj)
			param={'id':None,'student':student,'student_group':studentgroup,'academic':academic,'active':2}
			try:
				sgRelObj = Student_StudentGroupRelation.objects.get(student=student, student_group=studentgroup, academic=academic)
				sgRelObj.active=2
				sgRelObj.save()
			except:
				stdgrp_rels = Student_StudentGroupRelation(**param)
				stdgrp_rels.save()
			count = count+1
	return HttpResponseRedirect('/studentgroup/'+str(id)+'/view/?count='+str(count))

urlpatterns = patterns('',    
   url(r'^boundary/institution/(?P<referKey>.*)/studentgroup/creator/$', KLP_StudentGroup_Create),
   url(r'^studentgroup/(?P<studentgroup_id>\d+)/view/?$', KLP_StudentGroup_View),
   url(r'^studentgroup/(?P<studentgroup_id>\d+)/update/?$', KLP_StudentGroup_Update),
   url(r'^studentgroup/(?P<studentgroup_id>\d+)/programme/(?P<programme_id>\d+)/assessment/(?P<assessment_id>\d+)/view/?$', KLP_StudentGroup_Answer_Entry),
   url(r'^mapstudents/(?P<id>\d+)/$', MapStudents),
)
