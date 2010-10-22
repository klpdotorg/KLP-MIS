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

      
class SchoolView(Collection):    
    """ To view selected school details
    To view selected school boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/view/
    To edit selected school boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/edit/
    To create new school boundary/(?P<referKey>\d+)/schools/creator/"""
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
    """ To update School data boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/update/""" 
    def create(self,request,boundary_id, school_id):         
         school = School.objects.get(pk=school_id)    
         form =School_Form(request.POST, request.FILES,instance=school)         
         form.save()    
         respTemplate= render_to_response('viewtemplates/school_detail.html', {'school':school})
         return HttpResponse(respTemplate)


urlpatterns = patterns('',          
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/view/?$', template_school_view),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/edit/?$', template_school_edit),
   url(r'^boundary/(?P<referKey>\d+)/schools/creator/?$', template_school_view.responder.create_form, {'form_class':'school'}),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/update/?$', SchoolUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),
)
