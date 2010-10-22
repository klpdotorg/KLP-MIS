from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class ChildEntryView(Collection):   
    """ To create new Child child/(?P<referKey>\d+)/creator/""" 
    def get_entry(self,child_id):        
        child = Child.objects.get(id=child_id)
        return ChoiceEntry(self, child)

class ChildView(Collection):
    def get_entry(self, boundary_id, school_id, class_id, section_id, student_id):
        studentObj = student.objects.get(id=student_id)
	childObj = studentObj.name
        return ChoiceEntry(self, studentObj)

template_child_view =  ChildEntryView(
    queryset = Child.objects.filter(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'child',
    ),
  receiver = XMLReceiver(),
)

template_child_edit =  ChildView(
    queryset = student.objects.filter(active=True),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'studentObj'
    ),
  receiver = XMLReceiver(),
)

class ChildUpdate(Resource):
    """ To update Child boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/students/(?P<student_id>\d+)/update/"""
    def create(self, request, boundary_id, school_id, class_id, section_id, student_id):
        studentObj = student.objects.get(id=student_id)
	value = request.POST['academic']
	value = Academic_Year.objects.get(id = value)
	studentObj.__setattr__('academic', value)
        studentObj.save()
	childObj = Child.objects.get(id = studentObj.name.id)
        form =Child_Form(request.POST, request.FILES,instance=childObj)   
        form.save()
        respTemplate= render_to_response('prgtemplates/child_detail.html', {'childObj':childObj,'studentObj':studentObj,'class_id':class_id,'section_id':section_id})
        return HttpResponse(respTemplate)

urlpatterns = patterns('',
   url(r'^child/(?P<referKey>\d+)/creator/?$', template_child_view.responder.create_form, {'form_class':'child'}),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/students/(?P<student_id>\d+)/edit/?$', template_child_edit),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/students/(?P<student_id>\d+)/update/?$', ChildUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^child/(?P<child_id>\d+)/view/?$', template_child_view),
)
