from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class AcademicView(Collection):    
    """ To create new Academic Year academic/creator/"""  
    def get_entry(self,academic_id):        
        academic = Academic_Year.objects.all(id=academic_id)          
        return ChoiceEntry(self, academic)   

template_academic_view =  AcademicView(
    queryset = Academic_Year.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'academic',        
    ),
  receiver = XMLReceiver(),
)


urlpatterns = patterns('',             
   url(r'^academic/creator/?$', template_academic_view.responder.create_form, {'form_class':'academic'}),   
)
