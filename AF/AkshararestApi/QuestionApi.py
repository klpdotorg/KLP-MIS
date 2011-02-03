from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from django.http import HttpResponse
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

from schools.signals import check_user_perm
from schools.receivers import KLP_user_Perm

class KLP_Question(Collection):    
    """ To create new Question assessment/question/(?P<referKey>\d+)/creator/"""
    def get_entry(self,question_id):        
        question = Question.objects.get(id=question_id)          
        return ChoiceEntry(self, question)   
        


def KLP_Question_View(request, question_id):
	""" To View Selected Assessment question/(?P<question_id>\d+)/view/"""
	kwrg = {'is_entry':True}
	resp=KLP_Question(queryset = Question.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'question',),)(request, question_id, **kwrg)
        return HttpResponse(resp) 

        
def KLP_Question_Create(request, referKey):
	""" To Create New Assessment assessment/question/(?P<referKey>\d+)/creator/"""
	check_user_perm.send(sender=None, user=request.user, model='Question', operation='Add')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
        KLP_Create_Question = KLP_Question(queryset = Question.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'question', extra_context={'buttonType':buttonType, 'referKey':referKey}), receiver = XMLReceiver(),)
        response = KLP_Create_Question.responder.create_form(request,form_class=Question_Form)
        			
        return HttpResponse(response)               
        
def KLP_Question_Update(request, question_id):
	""" To update Selected Boundary question/(?P<question_id>\d+)/update/"""
	check_user_perm.send(sender=None, user=request.user, model='Question', operation='Update')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
	referKey = request.POST.get('form-0-assessment')
	KLP_Edit_Question =KLP_Question(queryset = Question.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'question', extra_context={'buttonType':buttonType, 'referKey':referKey}), receiver = XMLReceiver(),)
	response = KLP_Edit_Question.responder.update_form(request, pk=question_id, form_class=Question_Form)
	
	return HttpResponse(response)                  
        

urlpatterns = patterns('',             
   url(r'^assessment/question/(?P<referKey>\d+)/creator/?$', KLP_Question_Create),
   url(r'^question/(?P<question_id>\d+)/view/?$', KLP_Question_View),
   url(r'^question/(?P<question_id>\d+)/update/?$', KLP_Question_Update),
)
