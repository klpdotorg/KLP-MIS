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


class BoundaryView(Collection):
    """To get all boundary details
    To get all boundary details boundary/
    To get selected boundary details boundary/(?P<boundary_id>\d+)/view/
    To create new boundary boundary/creator/
    To edit particular boundary boundary/(?P<boundary_id>\d+)/edit/
    """
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

template_boundary_edit =  BoundaryView(
    queryset = Boundary.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'boundary',
    ),
  receiver = XMLReceiver(),
)

class BoundaryUpdate(Resource):    
    """ To update boundary data after edit
    To update boundary data boundary/(?P<boundary_id>\d+)/update/"""
    def create(self,request,boundary_id):         
         boundary = Boundary.objects.get(pk=boundary_id)    
         form =Boundary_Form(request.POST, request.FILES,instance=boundary)         
         form.save()    
         respTemplate= render_to_response('viewtemplates/boundary_detail.html', {'boundary':boundary})
         return HttpResponse(respTemplate)
         

class CreateNew(Resource):
    def read(self, request, model_name, new_id):
	objDict = {'boundary':Boundary, 'school':School, 'class':Class,'sections':Sections,'student':student, 'programme':Programme, 'assessment':Assessment, 'assessmentdetail':AssessmentDetail}
	modelObj = objDict[model_name]
        GetData = modelObj.objects.get(pk=new_id)
        return HttpResponse(GetData.CreateNewFolder())

class Delete(Resource):    
    """ To delete boundary boundary/(?P<boundary_id>\d+)/delete/"""
    def read(self,request,model_name, referKey):
        modelDict = {'boundary':Boundary, 'school':School, 'class':Class,'section':Sections,'student':student, 'programme':Programme, 'assessment':Assessment, 'assessmentdetail':AssessmentDetail}            
        obj = modelDict[model_name].objects.get(pk=referKey)   
        obj.active=0 
        obj.save()
        return HttpResponse('Deleted')

class BoundaryPartition(Resource):    
    """ To partiton boundary boundary/(?P<boundary_id>\d+)/partition/"""
    def read(self,request,boundary_id):            
         boundary = Boundary.objects.get(pk=boundary_id)           
         schoolsList = School.objects.filter(boundary=boundary,active=1)  
         respTemplate= render_to_response('viewtemplates/boundary_partition.html', {'boundary':boundary, 'schoolsList':schoolsList})
         return HttpResponse(respTemplate)
         
    def create(self,request,boundary_id):            
         boundary = Boundary.objects.get(pk=boundary_id)         
         selectedSchools = request.POST.getlist('schools')
         boundaryNew = Boundary(parent=boundary.parent, name=request.POST.get('newBoundary'), boundary_type=boundary.boundary_type, geo_code=boundary.geo_code,active=1)
         boundaryNew.save()
         for school in selectedSchools:
            schoolObj = School.objects.get(pk=str(school))
            schoolObj.boundary = boundaryNew
            schoolObj.save()                         
         return HttpResponse('success')              

urlpatterns = patterns('',
   url(r'^createnew/(?P<model_name>\w+)/(?P<new_id>\d+)/$', CreateNew(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^boundary/$', template_boundary_view),
   url(r'^boundary/(?P<boundary_id>\d+)/view/$', template_boundary_view),
   url(r'^boundary/creator/$', template_boundary_view.responder.create_form, {'form_class':'boundary'}),
   url(r'^boundary/(?P<boundary_id>\d+)/edit/$', template_boundary_edit),
   url(r'^boundary/(?P<boundary_id>\d+)/update/$', BoundaryUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^boundary/(?P<boundary_id>\d+)/partition/$', BoundaryPartition(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^delete/(?P<model_name>\w+)/(?P<referKey>\d+)/$', Delete(permitted_methods=('POST','PUT','GET','DELETE'))),
)
