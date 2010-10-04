from django.conf.urls.defaults import *
from django.http import HttpResponse
from django_restapi.resource import Resource
from Akshara.schools.models import *
from Akshara.schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class SectionView(Collection):    
    def get_entry(self, boundary_id, school_id, class_id, section_id):        
        section = Sections.objects.get(classname=class_id, id=section_id)
        return ChoiceEntry(self, section)     

template_section_view =  SectionView(
    queryset = Sections.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'section',        
    ),
  receiver = XMLReceiver(),
)

class SectionDelete(Resource):    
    def read(self,request,section_id):            
         section = Sections.objects.get(pk=section_id)   
         section.active=0 
         section.save()
         return HttpResponse('Deleted') 

urlpatterns = patterns('',            
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/view/?$', template_section_view),
   url(r'^classes/(?P<referKey>\d+)/section/creator/?$', template_section_view.responder.create_form, {'form_class':'section'}),
   url(r'^section/(?P<section_id>\d+)/delete/$', SectionDelete(permitted_methods=('POST','PUT','GET','DELETE'))),   
)
