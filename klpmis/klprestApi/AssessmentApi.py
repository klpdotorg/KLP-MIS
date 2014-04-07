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
from klprestApi.BoundaryApi import ChoiceEntry
import datetime
from django.shortcuts import render_to_response
from schools.receivers import KLP_user_Perm
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
class KLP_Assessment(Collection):    
    def get_entry(self,assessment_id):        
    	# Query For Selected assessment based on assessment_id
        assessment = Assessment.objects.get(id=assessment_id)          
        return ChoiceEntry(self, assessment)   
class KLP_Assessment_Lookup(Collection):    
    def get_entry(self,assessment_lookup_id):        
    	# Query For Selected assessment based on assessment_id
        assessment_lookup = Assessment_Lookup.objects.get(id=assessment_id)          
        return ChoiceEntry(self, assessment)   
        
def KLP_Assessment_View(request, assessment_id):
	""" To View Selected Assessment assessment/(?P<assessment_id>\d+)/view/"""
	kwrg = {'is_entry':True}
        assObj=Assessment.objects.filter(pk=assessment_id)
        copyEnable=True if (not Assessment_Lookup.objects.filter(assessment__id=assessment_id) and assObj[0].primary_field_type ==4 and assObj[0].flexi_assessment ) else False #before Assessment.objects.all()
	resp=KLP_Assessment(queryset = assObj, permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'assessment',extra_context={'copyEnable':copyEnable}),)(request, assessment_id, **kwrg)
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
        
        #before Assessment.objects.all()
        KLP_Create_Assessment = KLP_Assessment(queryset = Assessment.objects.filter(pk=0), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'assessment', extra_context={'buttonType':buttonType, 'referKey':referKey, 'end_date':30, 'endYear':endYear, 'endMonth':'APRIL'}), receiver = XMLReceiver(),)
        response = KLP_Create_Assessment.responder.create_form(request,form_class=Assessment_Form)
       		
        return HttpResponse(response)  
        
def KLP_Assessment_Lookup_Create(request, referKey):
	""" To Create New Assessment programme/assessment/(?P<referKey>\d+)/assessment_lookup_creator/"""
	# Checking user Permissions for Assessment add
	KLP_user_Perm(request.user, "Assessment", "Add")
	buttonType = request.POST.get('form-buttonType','')
	assessment_lookups = Assessment_Lookup.objects.filter(assessment__id = referKey).order_by('rank','name')
	if 1:
		
		#before Assessment.objects.all()
                rankrange=21
                if len(assessment_lookups)+1 >= rankrange:
                            rankrange=len(assessment_lookups)+2
		KLP_Create_Assessment = KLP_Assessment(queryset = Assessment_Lookup.objects.filter(pk=0), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'assessment_lookup', extra_context={'buttonType':buttonType, 'referKey':referKey,'rankrange':range(1,rankrange) ,'rank':len(assessment_lookups)+1}), receiver = XMLReceiver(),)
		response = KLP_Create_Assessment.responder.create_form(request,form_class=Assessment_Lookup_Form)
					
		return HttpResponse(response)  
                
def KLP_Assessment_Lookup_List(request, referKey):
	""" To View Selected StudentGroup studentsroup/(?P<areferKey>\d+)/view/?$"""
	reqlist= request.GET.items()
	itemlist=[str(k[0]) for k in reqlist]
	if 'count' in itemlist:
		count = request.GET['count']
	else:
		count = '0'
	kwrg = {'is_entry':True}
	
	url = '/assessment_lookup/'+referKey+'/multieditor/'
	assessment_lookups = Assessment_Lookup.objects.filter(assessment__id = referKey).order_by('rank','name')
	
	Norecords =assessment_lookups.count()
	
	resp=Collection(assessment_lookups, permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'assessement_lookup',paginate_by = 20,extra_context={'assessment_id':referKey,'referKey':referKey,'url':url, 'Norecords':Norecords, 'count':count}),)
	
        return HttpResponse(resp(request))
def KLP_Assessment_Lookup_Multieditor(request, assessment_id):
	""" To View Selected StudentGroup studentsroup/(?P<assessment_id>\d+)/edit/?$"""
	""" To show Bulk Students to update """
	assessment_lookupList = request.GET.getlist("assessment_lookup")
	
	return render_to_response('edittemplates/assessment_lookup_call_form.html',{'assessment_id':assessment_id, 'assessment_lookuplist':assessment_lookupList})	
	
def KLP_Assessment_Lookup_Update(request, referKey,assessment_lookup_id,counter=0):
	""" To update Selected Boundary assessment/(?P<assessment_id>\d+)/update/"""
	# Checking user Permissions for Assessment Update
	KLP_user_Perm(request.user, "Assessment", "Update")
        # Get Current date for to pass for calendar
	
	buttonType = request.POST.get('form-buttonType')
	
	extra_context={'buttonType':buttonType, 'referKey':referKey,'assessment_lookup_id':assessment_lookup_id,'counter':counter}
	
	KLP_Edit_Assessment =KLP_Assessment(queryset = Assessment_Lookup.objects.filter(pk=assessment_lookup_id).order_by('rank','name'), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'assessment_lookup', extra_context=extra_context), receiver = XMLReceiver(),)
	response = KLP_Edit_Assessment.responder.update_form(request, pk=assessment_lookup_id, form_class=Assessment_Lookup_Form)
	
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
	KLP_Edit_Assessment =KLP_Assessment(queryset = Assessment.objects.filter(pk=assessment_id), permitted_methods = ('GET', 'POST'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'assessment', extra_context={'buttonType':buttonType, 'referKey':referKey, 'end_date':30, 'endYear':endYear, 'endMonth':'APRIL'}), receiver = XMLReceiver(),)
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
from schools.forms import Assessment_Form,Question_Form
@csrf_exempt
def KLP_lookup_inlineEdit(request):
	lookupId=request.POST.get('lookupId',0)
	name=request.POST.get('name',0)
	des=request.POST.get('des',0)
	lookObj=Assessment_Lookup.objects.get(id=int(lookupId))
	lookObj.name=name
	lookObj.description=des
        lookObj.rank=request.POST.get('rank',0)
	try:
	  lookObj.save()
	except IntegrityError:
						return HttpResponse('Value is already existing')
	return HttpResponse('Data Saved')
import json
@csrf_exempt		
def KLP_Assessment_Lookup_Copy(request, referKey):
	""" To View Selected StudentGroup studentsroup/(?P<areferKey>\d+)/copy/?$'/assessment/assessment_lookup/'+stre(referKey+'/view',"""
	
	if request.POST:	
		assessmentId=request.POST.get('lookupValues')
		assessmentLookupList=Assessment_Lookup.objects.filter(assessment__id=assessmentId)
    
		for k in assessmentLookupList:
			k.id=None
			k.assessment_id=referKey
			k.save()
    
		return HttpResponse('Copied Successfully')
	else:
		assessmentLookupList=Assessment_Lookup.objects.filter().values_list('assessment',flat=True)
		assessmentList=Assessment.objects.filter(id__in=assessmentLookupList).exclude(id=referKey)
	
		return render_to_response('viewtemplates/assessment_lookup_copy.html',{'assessment_id':referKey, 'assessmentList':assessmentList})
	
@csrf_exempt
def KLP_copy_Assessments(request,assessment_id):
    """To copy the assessment"""
    Ass=Assessment.objects.filter(id=assessment_id)[0]
   
    if request.POST:
       try:
          KLP_user_Perm(request.user, "Assessment", "Create")
          Ass=Assessment.objects.filter(id=assessment_id).values()
          Assdic=Ass[0]
          del Assdic['id']
          Assdic['programme']=Assdic['programme_id']
          Assdic['name']=request.POST.get('newasssmentname','copy _of_')
          newAssForm=Assessment_Form(Assdic)
          newAss= newAssForm.save()
          QuObjects=Question.objects.filter(assessment__id=assessment_id).values()
          newquestionids=''
          for QuObject in QuObjects:
              del QuObject['id']
              QuObject['assessment']=newAss.id
              qq=Question_Form(QuObject)
              qqObj=qq.save()
              newquestionids+=str(qqObj.id)+','
          
            
          KLP_Assessment_Lookup_Copy(request,newAss.id)
    
          return HttpResponse('Succesfully Copied_'+str(newAss.id)+'_'+newquestionids)
       except:
                     return HttpResponse('Duplicate Assessment .')
    else:
         return render_to_response('viewtemplates/assessment_copy_form.html',{'assessment':Ass})
       
urlpatterns = patterns('',             
   url(r'^assessment/(?P<assessment_id>\d+)/view/?$', KLP_Assessment_View),   
   url(r'^programme/assessment/(?P<referKey>\d+)/creator/?$', KLP_Assessment_Create), 
	url(r'^programme/assessment/assessment_lookup/(?P<referKey>\d+)/creator/?$', KLP_Assessment_Lookup_Create), 
     url(r'^assessment/assessment_lookup/(?P<referKey>\d+)/copy/?$', KLP_Assessment_Lookup_Copy),
	url(r'^assessment/assessment_lookup/(?P<referKey>\d+)/view/?$', KLP_Assessment_Lookup_List),
	url(r'^assessment/assessment_lookup/(?P<assessment_id>\d+)/multieditor/?$', KLP_Assessment_Lookup_Multieditor),
   url(r'^assessment/(?P<assessment_id>\d+)/update/?$', KLP_Assessment_Update), 
    url(r'^assessment/(?P<referKey>\d+)/assessment_lookup/(?P<assessment_lookup_id>\d+)/update/?$', KLP_Assessment_Lookup_Update), 
	 url(r'^assessment/(?P<referKey>\d+)/assessment_lookup/(?P<assessment_lookup_id>\d+)/update/(?P<counter>\d+)/?$', KLP_Assessment_Lookup_Update), 
   url(r'^filter/programme/(?P<programme_id>\d+)/assessments/$', KLP_Get_Assessments(permitted_methods=('POST','GET'))),
    url(r'^assessment/(?P<assessment_id>\d+)/copy/?$', KLP_copy_Assessments),
	 url(r'^assessment_lookup_value/inlineedit/?$',KLP_lookup_inlineEdit),
)
