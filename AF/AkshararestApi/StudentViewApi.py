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

class StudentView(Collection):    
    """ To create new student  sections/(?P<referKey>\d+)/student/creator/ 
    To edit selected student boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/students/(?P<student_id>\d+)/edit/
    """
    def get_entry(self, boundary_id, school_id, class_id, section_id, student_id):
        studentObj = student.objects.get(class_section=section_id, id=student_id)
        return ChoiceEntry(self, studentObj)

template_student_view =  StudentView(
    queryset = student.objects.filter(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'studentObj',
    ),
  receiver = XMLReceiver(),
)

template_student_edit =  StudentView(
    queryset = student.objects.filter(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'studentObj',
    ),
  receiver = XMLReceiver(),
)

class StudentUpdate(Resource): 
    """ To update student data  boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/students/(?P<student_id>\d+)/update/"""   
    def create(self, request, boundary_id, school_id, class_id, section_id, student_id):
        studentObj = student.objects.get(id=student_id)
        form =Student_Form(request.POST, request.FILES,instance=studentObj)
        form.save()
        respTemplate= render_to_response('viewtemplates/student_detail.html', {'studentObj':studentObj})
        return HttpResponse(respTemplate)


urlpatterns = patterns('',
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/students/(?P<student_id>\d+)/view/?$', template_student_view),   
   #url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/students/(?P<student_id>\d+)/edit/?$', template_student_edit),
   #url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/students/(?P<student_id>\d+)/update/?$', StudentUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^sections/(?P<referKey>\d+)/student/creator/?$', template_student_view.responder.create_form, {'form_class':'student'}),
)
