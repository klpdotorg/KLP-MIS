from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from Akshara.schools.models import *
from Akshara.schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class ManagementView(Collection):    
    def get_entry(self,school_category_id):        
        management = School_Management.objects.all(id=management_id)          
        return ChoiceEntry(self, management)   

template_management_view =  ManagementView(
    queryset = School_Management.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'management',        
    ),
  receiver = XMLReceiver(),
)


urlpatterns = patterns('',             
   url(r'^school-management/creator/?$', template_management_view.responder.create_form, {'form_class':'management'}),   
)
