from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from Akshara.schools.models import *
from Akshara.schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class LanguageView(Collection):    
    def get_entry(self,language_id):        
        language = Moi_Type.objects.all(id=language_id)          
        return ChoiceEntry(self, language)   

template_language_view =  LanguageView(
    queryset = Moi_Type.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'language',        
    ),
  receiver = XMLReceiver(),
)


urlpatterns = patterns('',             
   url(r'^language/creator/?$', template_language_view.responder.create_form, {'form_class':'language'}),   
)
