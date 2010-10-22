from django.conf.urls.defaults import *
from django.http import HttpResponse
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class SectionView(Collection):    
    """ To create new section classes/(?P<referKey>\d+)/section/creator/""" 
    def get_entry(self, boundary_id, school_id, class_id, section_id):
        section = Sections.objects.get(classname=class_id, id=section_id,active=True)
        return ChoiceEntry(self, section)

template_section_view =  SectionView(
    queryset = Sections.objects.filter(active=True),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'section',
    ),
  receiver = XMLReceiver(),
)

template_question_assign =  SectionView(
    queryset = Sections.objects.filter(active=True),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'prgtemplates',
        template_object_name = 'section',
    ),
  receiver = XMLReceiver(),
)

class SectionDelete(Resource):
    """ To delete selected section section/(?P<section_id>\d+)/delete/""" 
    def read(self,request,section_id):
         section = Sections.objects.get(pk=section_id)
         section.active=0
         section.save()
         return HttpResponse('Deleted')

def SectionInfo(request, section_id):
	''' To display the Child details according to Pagination'''
	queryset = []
	queryset=Sections.objects.filter(id = section_id,active = True)
	val=Collection(queryset,
	permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
	responder = TemplateResponder(
	paginate_by = 4,
	template_dir = 'viewtemplates',
	template_object_name = 'section'
	),
	entry_class = ChoiceEntry,
	)
	return val

def SectionInfoView(request, boundary_id, school_id, class_id, section_id):
	''' To display the Child details according to Pagination'''
	queryset = []
	queryset=student.objects.filter(class_section__id = section_id,active = True, academic__id=current_academic)
	if queryset:
		val=Collection(queryset,
		permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),

		responder = TemplateResponder(
		paginate_by = 4,
		template_dir = 'viewtemplates',
		template_object_name = 'student'
		),
		entry_class = ChoiceEntry,
		)
	else:
        	val=SectionInfo(request,section_id)
	return HttpResponse(val(request))

urlpatterns = patterns('',
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/view/?$', SectionInfoView),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/sections/(?P<section_id>\d+)/question/student/?$', template_question_assign),
   url(r'^classes/(?P<referKey>\d+)/section/creator/?$', template_section_view.responder.create_form, {'form_class':'section'}),
   url(r'^section/(?P<section_id>\d+)/delete/$', SectionDelete(permitted_methods=('POST','PUT','GET','DELETE'))),
)
