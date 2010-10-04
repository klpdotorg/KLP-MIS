from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection, Entry, reverse
from django_restapi.responder import *
from Akshara.schools.models import Class
from django_restapi.resource import Resource
from Akshara.AkshararestApi.BoundaryApi import ChoiceEntry
from django_restapi.authentication import *
class ClassCollectionEntry(Collection):
    
    def read(self, request):
       
        ''' To get the Class details in selected school 

          to get the all class details list of selected class id either api/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/ or

          api/xml/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/
                  
         In json format api/json/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/'''
        
        filtered_set = self.queryset._clone()
        
        
        return self.responder.list(request, filtered_set)
    
    def get_entry(self, boundary_id,school_id,class_id):
        
        
        classname=Class.objects.get(sid=school_id,id=class_id)
        print classname
        
        return ChoiceEntry(self, classname)
class ClassCollection(Collection):
    
    def read(self, request):
       
       
        paths=request.path.split('/')
        ''' To get the Class details in selected school  

          to get the all class details list of selected school id either api/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/ or

          api/xml/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/
                  
         In json format api/json/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/'''
        for k in range(0,len(paths)):
           if paths[k]=='schools' and paths[k+2]=='classes':
                school_id=paths[k+1]
                break
        filtered_set = Class.objects.filter(sid__id__exact=int(school_id))
        
        
        return self.responder.list(request, filtered_set)
    
  

xml_choice_resourceentry = ClassCollectionEntry(
    queryset = Class.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
   
    responder = XMLResponder(paginate_by=5),
    entry_class = ChoiceEntry,
    authentication = HttpBasicAuthentication()
)
json_choice_resourceentry = ClassCollectionEntry(
    queryset = Class.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    
    responder = JSONResponder(paginate_by=5),
    entry_class = ChoiceEntry,
     authentication = HttpBasicAuthentication()
)
xml_choice_resource = ClassCollection(
    queryset = Class.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
   
    responder = XMLResponder(paginate_by=5),
    entry_class = ChoiceEntry,
    authentication = HttpBasicAuthentication()
)
json_choice_resource = ClassCollection(
    queryset = Class.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    
    responder = JSONResponder(paginate_by=5),
    entry_class = ChoiceEntry,
     authentication = HttpBasicAuthentication()
)
urlpatterns = patterns('',
    
   url(r'^api/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/?$', xml_choice_resourceentry),
   url(r'^api/xml/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/?$', xml_choice_resource,{'is_entry':False}),
   url(r'^api/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/?$', xml_choice_resource,{'is_entry':False}),
   url(r'^api/xml/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/?$', xml_choice_resource,{'is_entry':False}),
   url(r'^api/json/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/?$', json_choice_resource,{'is_entry':False}),
    url(r'^api/xml/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/?$', xml_choice_resourceentry),
   url(r'^api/json/boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/?$', json_choice_resourceentry),
   
)
