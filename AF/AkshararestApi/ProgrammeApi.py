from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class ProgrammeView(Collection):    
    """ To create new Programme programme/creator/"""
    def get_entry(self,programme_id):
        programme = Programme.objects.get(id=programme_id)
        return ChoiceEntry(self, programme)

template_programme_view =  ProgrammeView(
    queryset = Programme.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'programme',
    ),
  receiver = XMLReceiver(),
)

template_programme_edit =  ProgrammeView(
    queryset = Programme.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'programme',
    ),
  receiver = XMLReceiver(),
)

class ProgrammeUpdate(Resource):    
    """ To update programme data after edit
    To update programme data programme/(?P<programme_id>\d+)/update/"""
    def create(self,request,programme_id):
         programme = Programme.objects.get(pk=programme_id)
         form =Programme_Form(request.POST, request.FILES,instance=programme)
         form.save()    
         respTemplate= render_to_response('viewtemplates/programme_detail.html', {'programme':programme})
         return HttpResponse(respTemplate)


urlpatterns = patterns('',
   url(r'^programme/(?P<programme_id>\d+)/view/?$', template_programme_view, ),    
   url(r'^programme/creator/?$', template_programme_view.responder.create_form, {'form_class':'programme'}),
   url(r'^programme/(?P<programme_id>\d+)/edit/$', template_programme_edit),
   url(r'^programme/(?P<programme_id>\d+)/update/$', ProgrammeUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),
)
