from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection, Entry, reverse
from django_restapi.responder import *
from Akshara.schools.models import School
from django_restapi.resource import Resource
from Akshara.AkshararestApi.BoundaryApi import ChoiceEntry
from django_restapi.authentication import *
class SchoolsCollectionEntry(Collection):
    
    def read(self, request):
       
        
        ''' To get the selected school details in selected boundary  

          to get the all school list of selected boundary either api/boundary/(?P<boundary_id>\d+)/schools/<school_id> or

          api/xml/boundary/(?P<boundary_id>\d+)/schools/<school_id>
                  
         In json format api/json/boundary/(?P<boundary_id>\d+)/schools/<School_id>'''
        filtered_set = self.queryset._clone()
        
        
        return self.responder.list(request, filtered_set)
    
    def get_entry(self, boundary_id,school_id):
        
        schools = School.objects.get(id=int(school_id),boundary=boundary_id)
        print schools
        
        return ChoiceEntry(self, schools)

class SchoolsCollection(Collection):
    
    def read(self, request):
       
        
        paths=request.path.split('/')
        ''' To get the school details in selected boundary 

          to get the all school list of selected boundary either api/boundary/(?P<boundary_id>\d+)/schools/ or

          api/xml/boundary/(?P<boundary_id>\d+)/schools/
                  
         In json format api/json/boundary/(?P<boundary_id>\d+)/schools/'''
        for k in range(0,len(paths)):
           if paths[k]=='boundary' and paths[k+2]=='schools':
                boundary_id=paths[k+1]
                break
       
        filtered_set = School.objects.filter(boundary__id__exact=int(boundary_id))
        
       
        return self.responder.list(request, filtered_set)
    
   

xml_choice_resourceentry = SchoolsCollectionEntry(
    queryset = School.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
   
    responder = XMLResponder(paginate_by=5),
    entry_class = ChoiceEntry,
    authentication = HttpBasicAuthentication()
)
json_choice_resourceentry = SchoolsCollectionEntry(
    queryset = School.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    
    responder = JSONResponder(paginate_by=5),
    entry_class = ChoiceEntry,
     authentication = HttpBasicAuthentication()
)
xml_choice_resource = SchoolsCollection(
    queryset = School.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
   
    responder = XMLResponder(paginate_by=5),
    entry_class = ChoiceEntry,
    authentication = HttpBasicAuthentication()
)
json_choice_resource = SchoolsCollection(
    queryset = School.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    
    responder = JSONResponder(paginate_by=5),
    entry_class = ChoiceEntry,
     authentication = HttpBasicAuthentication()
)
urlpatterns = patterns('',
    url(r'^api/boundary/(?P<boundary_id>\d+)/schools/?$', xml_choice_resource,{'is_entry':False}),
    url(r'^api/xml/boundary/(?P<boundary_id>\d+)/schools/?$', xml_choice_resource,{'is_entry':False}),
   url(r'^api/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/?$', xml_choice_resourceentry),
   url(r'^api/xml/boundary/(?P<boundary_id>\d+)/schools/?$', xml_choice_resource,{'is_entry':False}),
    url(r'^api/xml/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/?$', xml_choice_resourceentry),
   url(r'^api/json/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/?$', json_choice_resourceentry),
   
)
