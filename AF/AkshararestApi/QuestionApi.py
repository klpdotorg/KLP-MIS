from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class QuestionView(Collection):
    """ To create new Question question/creator/"""
    def get_entry(self,question_id):
        question = Question.objects.get(id=question_id)
        return ChoiceEntry(self, question)

template_question_view =  QuestionView(
    queryset = Question.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'question',
    ),
  receiver = XMLReceiver(),
)


urlpatterns = patterns('',
   url(r'^question/creator/?$', template_question_view.responder.create_form, {'form_class':'question'}),
   url(r'^question/(?P<question_id>\d+)/view/?$', template_question_view) 
)
