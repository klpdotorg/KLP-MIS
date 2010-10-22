from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry



class AssessmentDetailView(Collection):    
    """ To create new Assessment assessment/creator/"""
    def get_entry(self,assessmentdetail_id):        
        assessmentDetail = AssessmentDetail.objects.get(id=assessmentdetail_id)          
        return ChoiceEntry(self, assessmentDetail)   

template_assessmentdetail_view =  AssessmentDetailView(
    queryset = AssessmentDetail.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'assessmentDetail',        
    ),
  receiver = XMLReceiver(),
)

template_assessmentdetail_edit = AssessmentDetailView(
    queryset = AssessmentDetail.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'assessmentDetail',        
    ),
  receiver = XMLReceiver(),
)    

class AssessmentDetailUpdate(Resource):
    """ To update AssessmentDetail data after edit
    To update AssessmentDetail data assessmentdetail/(?P<assessmentdetail_id>\d+)/update/"""
    def create(self,request,assessmentdetail_id):
        asdObj = AssessmentDetail.objects.get(pk=assessmentdetail_id)    
        form =AssessmentDetail_Form(request.POST, request.FILES,instance=asdObj)         
        form.save()    
        respTemplate= render_to_response('viewtemplates/assessmentdetail_detail.html', {'assessmentDetail':asdObj})
        return HttpResponse(respTemplate)



urlpatterns = patterns('',             
   url(r'^assessmentdetail/(?P<referKey>\d+)/creator/?$', template_assessmentdetail_view.responder.create_form, {'form_class':'assessmentDetail'}),
   url(r'^assessmentdetail/(?P<assessmentdetail_id>\d+)/view/?$', template_assessmentdetail_view),
   url(r'^assessmentdetail/(?P<assessmentdetail_id>\d+)/edit/?$', template_assessmentdetail_edit),
   url(r'^assessmentdetail/(?P<assessmentdetail_id>\d+)/update/?$', AssessmentDetailUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),
)
