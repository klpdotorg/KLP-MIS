from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *


from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory

from schools.signals import check_user_perm
from schools.receivers import KLP_user_Perm


class ChoiceEntry(Entry):
      pass

class KLP_Boundary(Collection):
    """To get all boundary details
    To get all boundary details boundary/
    To create new boundary boundary/creator/
    To edit particular boundary boundary/(?P<boundary_id>\d+)/edit/
    """
    def get_entry(self, boundary_id):        
        boundary = Boundary.objects.get(id=int(boundary_id))
        return ChoiceEntry(self, boundary)     
  

def KLP_Boundary_View(request, boundary_id, boundarytype_id):
	""" To View Selected Boundary boundary/(?P<boundary_id>\d+)/(?P<boundarytype_id>\d+)/view/$"""
	kwrg = {'is_entry':True}
	boundaryTypObj = Boundary_Type.objects.get(pk = boundarytype_id)
	resp=KLP_Boundary(queryset = Boundary.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'boundary', extra_context={'boundary_type':boundaryTypObj.boundary_type}),)(request, boundary_id, **kwrg)
        return HttpResponse(resp)  


def KLP_Boundary_Create(request):
	""" To Create New Boundary boundary/creator/"""
	check_user_perm.send(sender=None, user=request.user, model='Boundary', operation='Add')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
        KLP_Create_Boundary =KLP_Boundary(queryset = Boundary.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'boundary', extra_context={'buttonType':buttonType}), receiver = XMLReceiver(),)
        
	response = KLP_Create_Boundary.responder.create_form(request,form_class=Boundary_Form)
	
	return HttpResponse(response)
	
def KLP_Boundary_Update(request, boundary_id):
	""" To update Selected Boundary boundary/(?P<boundary_id>\d+)/update/"""
	check_user_perm.send(sender=None, user=request.user, model='Boundary', operation='Update')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
	referKey = request.POST.get('form-0-boundary')
	KLP_Edit_Boundary =KLP_Boundary(queryset = Boundary.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'boundary', extra_context={'buttonType':buttonType, 'referKey':referKey}), receiver = XMLReceiver(),)
	response = KLP_Edit_Boundary.responder.update_form(request, pk=boundary_id, form_class=Boundary_Form)
	
	return HttpResponse(response)

class KLP_Create_Node(Resource):
    def read(self, request, model_name, new_id):
	objDict = {'boundary':Boundary, 'institution':Institution, 'programme':Programme, 'assessment':Assessment, 'question':Question, 'studentgroup':StudentGroup, 'student':Student}
	boundaryType =  request.GET.get('boundaryType')
	modelObj = objDict[model_name]
        GetData = modelObj.objects.get(pk=new_id)
	if model_name == 'boundary':
		return HttpResponse(GetData.CreateNewFolder(boundaryType))
        return HttpResponse(GetData.CreateNewFolder())

class KLP_Delete(Resource):    
    """ To delete boundary boundary/(?P<boundary_id>\d+)/delete/"""
    def read(self,request,model_name, referKey):
        modelDict = {'boundary':Boundary, 'institution':Institution, 'programme':Programme, 'assessment':Assessment, 'question':Question, 'studentgroup':StudentGroup, 'student':Student, 'staff':Staff, 'class':StudentGroup, 'center':StudentGroup}
        check_user_perm.send(sender=None, user=request.user, model=modelDict[model_name.lower()], operation='Delete')
        check_user_perm.connect(KLP_user_Perm)
        obj = modelDict[model_name.lower()].objects.get(pk=referKey)
	if model_name == 'student':
		Student_StudentGroupRelation.objects.filter(student__id = referKey).update(active=0)
        obj.active=0 
        obj.save()
        return HttpResponse('Deleted')


urlpatterns = patterns('',
   url(r'^boundary/(?P<boundary_id>\d+)/(?P<boundarytype_id>\d+)/view/$', KLP_Boundary_View),
   url(r'^boundary/creator/?$', KLP_Boundary_Create),
   url(r'^boundary/(?P<boundary_id>\d+)/update/$', KLP_Boundary_Update),
   url(r'^delete/(?P<model_name>\w+)/(?P<referKey>\d+)/$', KLP_Delete(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^createnew/(?P<model_name>\w+)/(?P<new_id>\d+)/$', KLP_Create_Node(permitted_methods=('POST','PUT','GET','DELETE'))),
   
   
)
