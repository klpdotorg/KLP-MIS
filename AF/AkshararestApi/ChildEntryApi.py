from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from Akshara.schools.models import *
from Akshara.schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class ChildEntryView(Collection):    
    def get_entry(self,child_id):        
        child = Child.objects.all(id=child_id)          
        return ChoiceEntry(self, child)   

template_child_view =  ChildEntryView(
    queryset = Child.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'child',        
    ),
  receiver = XMLReceiver(),
)


urlpatterns = patterns('',             
   url(r'^child/(?P<referKey>\d+)/creator/?$', template_child_view.responder.create_form, {'form_class':'child'}),   
)
