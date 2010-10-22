from django.conf.urls.defaults import *
from django.http import HttpResponse
from django_restapi.resource import Resource
from schools.models import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.AutoCompleteResponder import AutoJSONResponder


class AutoCompleteInfo(Resource):
    """ To Generate Matching results for auto complete  get-info/"""
    def read(self,request):
        CategoryDic={'cat':School_Category,'school_type':School_Type,'moi':Moi_Type,'mgmt':School_Management}
        key_value = request.GET.get('q')
        if len(key_value)==0:
            return HttpResponse(0)
        fieldName = request.GET.get('fieldName')
        Database = int(request.GET.get('Database'))
        extraParam = int(request.GET.get('extraPram'))        
        fiedNames = {'boundary':'name','boundary_type':'boundary_type','child':'firstName','school':'name','question':'question'}          
        respDict = {'query':str(key_value), 'fieldName':str('id_'+fieldName),'field':fiedNames[fieldName]}        
        if fieldName == 'boundary_type':
            query = Boundary_Type.objects.filter(boundary_type__startswith=key_value)    
        if fieldName == 'boundary':
            query = Boundary.objects.filter(name__startswith=key_value)
        if fieldName == 'question':
            query = Question.objects.filter(question__startswith=key_value)
        if fieldName == 'school':
            query = School.objects.filter(name__startswith=key_value)       
        if fieldName == 'child':   
            sectionObj = Sections.objects.get(pk=extraParam)
            query = Child.objects.filter(firstName__startswith=key_value,boundary=sectionObj.classname.sid.boundary)   
        val= Collection(queryset = query, responder = AutoJSONResponder(respDict=respDict))        
        return HttpResponse(val(request),mimetype="application/json")
        
urlpatterns = patterns('',             
   url(r'^get-info/$', AutoCompleteInfo(permitted_methods=('POST','PUT','GET','DELETE'))),   
)
