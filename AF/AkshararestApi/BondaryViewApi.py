from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from Akshara.schools.models import *
from Akshara.schools.models import *
from Akshara.schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
# Urls for a resource that does not map 1:1 
# to Django models.

from django.forms import ModelForm
from django import forms

class BoundaryView(Collection):
    
    def get_entry(self, boundary_id):        
        boundary = Boundary.objects.get(id=int(boundary_id))
        return ChoiceEntry(self, boundary)     
  

template_boundary_view =  BoundaryView(
    queryset = Boundary.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'boundary',
                
    ),
  receiver = XMLReceiver(),
)
class BoundarySave(Resource):
    def read(self,request,boundary_id):
       
         s=Boundary(request.POST)
         s.save() 
         
    def create(self,request,boundary_id):
         print request.POST,'***********************************************'
         param=request.POST.urlencode().replace('&',',')
         param = param.replace('on','1')
         print param
         boundary = Boundary.objects.get(pk=boundary_id)    
         form =Boundary_Form(request.POST, request.FILES,instance=boundary)
         #s=Boundary(geo_code=12342,name='Bangalore',parent=1,boundary_type=2,active=1,csrfmiddlewaretoken='3fb75299fabdf19f11e26f0927b7ca09')
         form.save()    
         n= render_to_response('viewtemplates/boundary_detail.html', {'boundary':boundary})
         return HttpResponse(n)
          
'''    
template_boundary_save =  BoundarySave(
    queryset = Boundary.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder =  JSONResponder(paginate_by=5),
  receiver = XMLReceiver(),
)
'''
class BoundaryEdit(Collection):      
    def get_entry(self, boundary_id):        
        boundary = Boundary.objects.get(id=int(boundary_id))
        return ChoiceEntry(self, boundary)  

template_boundary_edit =  BoundaryEdit(
    queryset = Boundary.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'boundary',
                
    ),
  receiver = XMLReceiver(),
)

class ChoiceEdit(Entry):
      pass
      
class SchoolView(Collection):    
    def get_entry(self, boundary_id, school_id):        
        school = School.objects.get(boundary=boundary_id, id=school_id)
        #form = School_Form(instance=school)
        #return ChoiceEdit(self, school)  
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


class ClassView(Collection):    
    def get_entry(self, boundary_id, school_id, class_id):        
        classObj = Class.objects.get(sid=school_id, id=class_id)
        return ChoiceEntry(self, classObj)     

template_class_view =  ClassView(
    queryset = Class.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'classObj',        
    ),
  receiver = XMLReceiver(),
)


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

class StudentView(Collection):    
    def get_entry(self, boundary_id, school_id, class_id, section_id, student_id):        
        studentObj = student.objects.get(class_section=section_id, id=student_id)
        return ChoiceEntry(self, studentObj)     

template_student_view =  StudentView(
    queryset = student.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'studentObj',        
    ),
  receiver = XMLReceiver(),
)

urlpatterns = patterns('',
   url(r'^boundary/$', template_boundary_view),
   url(r'^boundary/(?P<boundary_id>\d+)/view/$', template_boundary_view),
   url(r'^boundary/(?P<boundary_id>\d+)/save/$', BoundarySave(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^boundary/(?P<boundary_id>\d+)/edit/$', template_boundary_edit),       
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/view/?$', template_school_view),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/edit/?$', template_school_edit),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/?$', template_class_view),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/?$', template_section_view),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/students/(?P<student_id>\d+)/?$', template_student_view),
   #url(r'^api/template/boundary/(?P<boundary_id>\d+)/$', BoundaryViewCollection1(permitted_methods=('GET','DELETE'))),
)
