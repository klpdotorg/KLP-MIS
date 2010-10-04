from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from Akshara.schools.models import *
from Akshara.schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
# Urls for a resource that does not map 1:1 
# to Django models.

      
class SchoolView(Collection):    
    def get_entry(self, boundary_id, school_id):        
        school = School.objects.get(boundary=boundary_id, id=school_id)          
        return ChoiceEntry(self, school)   

template_school_view =  SchoolView(
    queryset = School.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'school',        
    ),
  receiver = XMLReceiver(),
)

template_school_edit =  SchoolView(
    queryset = School.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'school',        
    ),
  receiver = XMLReceiver(),
)

class SchoolUpdate(Resource):    
    def create(self,request,boundary_id, school_id):         
         school = School.objects.get(pk=school_id)    
         form =School_Form(request.POST, request.FILES,instance=school)         
         form.save()    
         respTemplate= render_to_response('viewtemplates/school_detail.html', {'school':school})
         return HttpResponse(respTemplate)
         
class SchoolDelete(Resource):    
    def read(self,request,school_id):            
         schoolObj = School.objects.get(pk=school_id)   
         schoolObj.active=0 
         schoolObj.save()
         return HttpResponse('Deleted')
         


urlpatterns = patterns('',          
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/view/?$', template_school_view),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/edit/?$', template_school_edit),
   url(r'^boundary/(?P<referKey>\d+)/schools/creator/?$', template_school_view.responder.create_form, {'form_class':'school'}),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/update/?$', SchoolUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^school/(?P<school_id>\d+)/delete/$', SchoolDelete(permitted_methods=('POST','PUT','GET','DELETE'))),   
)
