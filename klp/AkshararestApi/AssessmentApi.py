"""
Assessment Api file is used 
1) To view Assessment Details
2) To Create new assessment
3) To Update existing assessment
4) To get list of assessment while filtering based on programme in filter by programme link
"""
from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
import datetime

from schools.receivers import KLP_user_Perm

class KLP_Assessment(Collection):    
    def get_entry(self,assessment_id):        
    	# Query For Selected assessment based on assessment_id
        assessment = Assessment.objects.get(id=assessment_id)          
        return ChoiceEntry(self, assessment)   

        
def KLP_Assessment_View(request, assessment_id):
	""" To View Selected Assessment assessment/(?P<assessment_id>\d+)/view/"""
	kwrg = {'is_entry':True}
        #before Assessment.objects.all()
	resp=KLP_Assessment(queryset = Assessment.objects.filter(pk=assessment_id), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'assessment',),)(request, assessment_id, **kwrg)
        return HttpResponse(resp)       
        
        
def KLP_Assessment_Create(request, referKey):
	""" To Create New Assessment programme/assessment/(?P<referKey>\d+)/creator/"""
	# Checking user Permissions for Assessment add
	KLP_user_Perm(request.user, "Assessment", "Add")
        # Get Current date for to pass for calendar
	now = datetime.date.today()
	buttonType = request.POST.get('form-buttonType')
	currentMont = int(now.strftime('%m'))
	endYear = int(now.strftime('%Y'))
	if currentMont>4:
		endYear = endYear + 1 
        print referKey
        #before Assessment.objects.all()
        KLP_Create_Assessment = KLP_Assessment(queryset = Assessment.objects.filter(pk=0), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'assessment', extra_context={'buttonType':buttonType, 'referKey':referKey, 'endDate':30, 'endYear':endYear, 'endMonth':'APRIL'}), receiver = XMLReceiver(),)
        response = KLP_Create_Assessment.responder.create_form(request,form_class=Assessment_Form)
        print response  			
        return HttpResponse(response)  
        
        
def KLP_Assessment_Update(request, assessment_id):
	""" To update Selected Boundary assessment/(?P<assessment_id>\d+)/update/"""
	# Checking user Permissions for Assessment Update
	KLP_user_Perm(request.user, "Assessment", "Update")
        # Get Current date for to pass for calendar
	now = datetime.date.today()
	buttonType = request.POST.get('form-buttonType')
	referKey = request.POST.get('form-0-programme')
	currentMont = int(now.strftime('%m'))
	endYear = int(now.strftime('%Y'))
	if currentMont>4:
		endYear = endYear + 1
        #before Assessment.objects.all()
	KLP_Edit_Assessment =KLP_Assessment(queryset = Assessment.objects.filter(pk=assessment_id), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'assessment', extra_context={'buttonType':buttonType, 'referKey':referKey, 'endDate':30, 'endYear':endYear, 'endMonth':'APRIL'}), receiver = XMLReceiver(),)
	response = KLP_Edit_Assessment.responder.update_form(request, pk=assessment_id, form_class=Assessment_Form)
	
	return HttpResponse(response)                


class KLP_Get_Assessments(Resource):    
    """ To get  assessment under programme filter/programme/(?P<programme_id>\d+)/assessments/"""
    def read(self,request,programme_id):     
         try:     
            # Query all active(2) assessments based on programme id
            assessments_list = Assessment.objects.filter(programme__id=programme_id, active=2).defer("programme")
            respStr = ''
            for assessment in assessments_list:
                respStr += '%s$$%s&&' %(assessment.id, assessment)
            # slice string to remove "&&" added at last of string    
            return HttpResponse(respStr[0:len(respStr)-2])         
         except:
            return HttpResponse('fail')	          



urlpatterns = patterns('',             
   url(r'^assessment/(?P<assessment_id>\d+)/view/?$', KLP_Assessment_View),   
   url(r'^programme/assessment/(?P<referKey>\d+)/creator/?$', KLP_Assessment_Create),   
   url(r'^assessment/(?P<assessment_id>\d+)/update/?$', KLP_Assessment_Update), 
   url(r'^filter/programme/(?P<programme_id>\d+)/assessments/$', KLP_Get_Assessments(permitted_methods=('POST','GET'))),
)
