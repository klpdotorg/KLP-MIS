from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_restapi.responder import *
from django_restapi.receiver import *
from schools.models import *

from schools.signals import check_user_perm
from schools.receivers import KLP_user_Perm
from fullhistory.models import FullHistory
from django.db.models import Q
import datetime
from django.contrib.contenttypes.models import ContentType

def KLP_audit(request):
    user = request.user     
    check_user_perm.send(sender=None, user=user, model='Audit', operation=None)
    check_user_perm.connect(KLP_user_Perm)
    userList = User.objects.filter(is_active=1)
    respDict = {'userList':userList, 'title':'Karanataka Learning Partnership'}
    if request.POST:
    	selUser = request.POST.get('selUser')
    	defaultDate = datetime.date.today().strftime("%d")+'-'+datetime.date.today().strftime("%m")+'-'+datetime.date.today().strftime("%Y")
    	startDate = request.POST.get('startDate')
    	endDate = request.POST.get('endDate')
    	if not startDate:
    		startDate = defaultDate
    	if not endDate:
    		endDate = defaultDate
    	respDict['startDate'] = startDate
    	respDict['endDate'] = endDate
    	respDict['selUser'] = int(selUser)
    	strDate = startDate.split('-')
    	enDate = endDate.split('-')
    	fullHistoryList = FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=selUser)
    	respDict['fullHistoryList'] = fullHistoryList
    	return render_to_response('viewtemplates/auditTrial.html',respDict,context_instance=RequestContext(request)) 
    return render_to_response('viewtemplates/auditTrial.html',respDict,context_instance=RequestContext(request)) 
        
 
def  KLP_dEHistory(request):
    user = request.user     
    #check_user_perm.send(sender=None, user=user, model='Audit', operation=None)
    #check_user_perm.connect(KLP_user_Perm)
    userList = User.objects.filter(is_active=1)
    respDict = {'title':'Karanataka Learning Partnership'}
    contentList = ['institution', 'student', 'staff']
    if request.POST:
    	selUser = request.POST.get('selUser')
    	defaultDate = datetime.date.today().strftime("%d")+'-'+datetime.date.today().strftime("%m")+'-'+datetime.date.today().strftime("%Y")
    	startDate = request.POST.get('startDate')
    	endDate = request.POST.get('endDate')
    	if not startDate:
    		startDate = defaultDate
    	if not endDate:
    		endDate = defaultDate
    	respDict['startDate'] = startDate
    	respDict['endDate'] = endDate
    	strDate = startDate.split('-')
    	enDate = endDate.split('-')
    	deDict = {}
    	activePrgs = Programme.objects.filter(active=2).values_list("id", flat=True)
    	assessments = Assessment.objects.filter(programme__id__in=activePrgs, active=2).distinct()
    	respDict['assessments'] = assessments
    	for user in userList:
    		actDict = {}
    		for content in contentList:
    			contObj = ContentType.objects.get(app_label='schools', name=content)
    			actDict[content+'_c'] = len(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, content_type__id=contObj.id, action='C'))
    			actDict[content+'_u'] = len(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, content_type__id=contObj.id, action='U'))
    		for assessment in assessments:
    			questions = Question.objects.filter(assessment = assessment,active=2).values_list("id", flat=True).distinct()
    			answers = Answer.objects.filter(question__id__in=questions).values_list("id", flat=True).distinct()
    			if len(answers) == 0:
    				actDict[assessment.name] = 0
    				actDict[assessment.name+'_u'] = 0
    			else:	
    				nList = [i for i in answers]
    				actDict[assessment.name] = len(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, object_id__in=nList, action='C'))
    			 	actDict[assessment.name+'_u'] = len(FullHistory.objects.filter(action_time__gte=datetime.date(int(strDate[2]), int(strDate[1]), int(strDate[0])), action_time__lte=datetime.date(int(enDate[2]), int(enDate[1]), int(enDate[0])), request__user_pk=user.id, object_id__in=nList, action='U', _data__icontains='answer'))
    			
    		
    		deDict[user.username]=actDict
    	respDict['deDict'] = deDict
    	return render_to_response('viewtemplates/dEHistory.html',respDict,context_instance=RequestContext(request)) 
    return render_to_response('viewtemplates/dEHistory.html',respDict,context_instance=RequestContext(request)) 
    
    
urlpatterns = patterns('',           
   url(r'^audit/trial/$', KLP_audit),
   url(r'^dEHistory/$', KLP_dEHistory),
)    
