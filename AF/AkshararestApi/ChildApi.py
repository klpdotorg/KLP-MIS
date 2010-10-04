from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection, Entry, reverse
from django_restapi.responder import *
from Akshara.schools.models import Child
from django_restapi.resource import Resource
from Akshara.AkshararestApi.BoundaryApi import ChoiceEntry
from django_restapi.authentication import *

class ChildCollectionentry(Collection):
    
    def read(self, request):
        ''' To get the Child details 
         using url api/child/<child_id>

         In json format api/json/child/<child_id>

         In XML format either api/xml/child/<child_id>
         or api/child/<child_id>'''
         
        filtered_set = self.queryset._clone()
   
        return self.responder.list(request, filtered_set)
    
    def get_entry(self, child_id):
        
       
        child=Child.objects.get(id=child_id)

        return ChoiceEntry(self, child)

class ChildCollectionentryByName(Collection):
    
    def read(self, request):
       
        
       child=[] 
       ''' To get the Child details by category 

          name wise to get the child details list either api/child/name/<child-name> or api/xml/child/name/<child-name>
                  
         In json format api/json/child/name/<child-name>

         date of birth wise to get the child details list either api/child/dob/yyyymmdd or api/child/dob/yyyymmdd
                  
         In json format api/json/child/dob/yyyymmdd

         sex wise to get the child details list either api/child/sex/male or api/child/sex/female
                  
         In json format api/json/child/sex/male

            
         mother language wise to get the child details list either api/child/ml/1 or api/child/ml/2
                  
         In json format api/json/ml/1

         '''
        
       paths=request.path.split('/')
       child_name=paths[-1]
       field_name=paths[len(paths)-2]
       print child_name,'chname'
       print field_name
       if field_name=='name':
          child=Child.objects.filter(name__startswith=child_name)
       if field_name=='dobyear':
            
             child=Child.objects.filter(dob__year=child_name)
       if field_name=='dob':
             child_year=child_name[0:4]+'-'+child_name[4:6]+'-'+child_name[6:8]
             print child_year
             child=Child.objects.filter(dob=child_year)
       if field_name=='sex':
             child=Child.objects.filter(sex__startswith=child_name)
       if field_name=='ml':
             child=Child.objects.filter(mt=child_name)
       filtered_set=child
       
       return self.responder.list(request, filtered_set)
   


xml_choice_resource = Collection(
    queryset = Child.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
   
    responder = XMLResponder(paginate_by=5),
    entry_class = ChoiceEntry,
    authentication = HttpBasicAuthentication()
)


'''To get the all Child'''

json_choice_resource = Collection(
    queryset = Child.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    
    responder = JSONResponder(paginate_by=5),
    entry_class = ChoiceEntry,
     authentication = HttpBasicAuthentication()
)


xml_choice_resourceentry = ChildCollectionentry(
    queryset = Child.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
   
    responder = XMLResponder(paginate_by=5),
    entry_class = ChoiceEntry,
    authentication = HttpBasicAuthentication()
)
json_choice_resourceentry = ChildCollectionentry(
    queryset = Child.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    
    responder = JSONResponder(paginate_by=5),
    entry_class = ChoiceEntry,
     authentication = HttpBasicAuthentication()
)
xml_choice_resourceentrybyname = ChildCollectionentryByName(
    queryset = Child.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
   
    responder = XMLResponder(paginate_by=5),
    entry_class = ChoiceEntry,
    authentication = HttpBasicAuthentication()
)
json_choice_resourceentrybyname = ChildCollectionentryByName(
    queryset = Child.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    
    responder = JSONResponder(paginate_by=5),
    entry_class = ChoiceEntry,
     authentication = HttpBasicAuthentication()
)

urlpatterns = patterns('',
    
   url(r'^api/child/?$', xml_choice_resource),
   url(r'^api/xml/child/?$', xml_choice_resource),
   url(r'^api/json/child/?$', json_choice_resource),

  url(r'^api/child/(?P<child_id>\d+)/?$', xml_choice_resourceentry),
   url(r'^api/xml/child/(?P<child_id>\d+)/?$', xml_choice_resourceentry),
   url(r'^api/json/child/(?P<child_id>\d+)/?$', json_choice_resourceentry),
  url(r'^api/child/(?P<field_name>\w+)/(?P<child_name>\w+)/?$', xml_choice_resourceentrybyname, {'is_entry':False}),
   url(r'^api/xml/child/(?P<field_name>\w+)/(?P<child_name>\w+)/?$', xml_choice_resourceentrybyname, {'is_entry':False}),
   url(r'^api/json/child/(?P<field_name>\w+)/(?P<child_name>\w+)/?$', json_choice_resourceentrybyname, {'is_entry':False}),
 
   
)
