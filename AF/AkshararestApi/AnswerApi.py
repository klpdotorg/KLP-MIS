from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
# Urls for a resource that does not map 1:1 
# to Django models.
from django_restapi.authentication import *

def getStudentAnswers(request,student_id):
	
	queryset = []
	queryset=Answer.objects.filter(student__id=student_id)
	val=Collection(queryset,
	permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
	responder = TemplateResponder(
	paginate_by = 1,
	template_dir = 'viewtemplates',
	template_object_name = 'answer'
	),
	entry_class = ChoiceEntry,
	
	)
	return HttpResponse(val(request))


class answerEdit(Collection):    
    def get_entry(self, answer_id):        
        answerObj = Answer.objects.get(id=answer_id)
        print answerObj.id, answerObj.answer
        return ChoiceEntry(self, answerObj)

template_answer_edit =  answerEdit(
    queryset = Answer.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'answerObj'
    ),
  receiver = XMLReceiver(),
)

class AnswerEdit(Resource):    
    """ To create new Question question/creator/"""
    def read(self,request,answer_id):            
        answerObj = Answer.objects.get(pk=answer_id)
	answer = request.GET['answer']
	answerObj.answer = answer
	answerObj.save()
        return HttpResponse('saved')

urlpatterns = patterns('',          
   url(r'^answer/(?P<student_id>\d+)/view/?$', getStudentAnswers),
   url(r'^answer/(?P<answer_id>\d+)/edit/?$', AnswerEdit(permitted_methods=('POST','PUT','GET','DELETE'))),

)
