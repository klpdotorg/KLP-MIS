from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection, Entry, reverse
from django_restapi.responder import *
from Akshara.schools.models import Boundary_Type, Boundary
from django_restapi.resource import Resource

from django_restapi.authentication import *
class BoundaryCollection(Collection):
    
    def read(self, request):
       
         ''' To get the all boundary details  

          to get the all boundary list details either api/boundary/ or

          api/xml/boundary/
                  
         In json format api/json/boundary/


         to get the selected boundary details either api/boundary/(?P<boundary_id>\d+)/ or

          api/xml/boundary/(?P<boundary_id>\d+)/
                  
         In json format api/json/boundary/(?P<boundary_id>\d+)/'''
        
         filtered_set = self.queryset._clone()
        
        
         return self.responder.list(request, filtered_set)
    
    def get_entry(self, boundary_id):
        print boundary_id,'sss'
        poll = Boundary.objects.get(id=int(boundary_id))
        print poll
        
        return ChoiceEntry(self, poll)
   
class ChoiceEntry(Entry):
      pass

xml_choice_resource = BoundaryCollection(
    queryset = Boundary.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    expose_fields = ('id','parent_id','name','boundary_type','geo_code','active'),
    responder = XMLResponder(paginate_by=5),
    entry_class = ChoiceEntry,
    authentication = HttpBasicAuthentication()
)
json_choice_resource = BoundaryCollection(
    queryset = Boundary.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    expose_fields = ('id','parent_id','name','boundary_type','geo_code','active'),
    responder = JSONResponder(paginate_by=5),
    entry_class = ChoiceEntry,
     authentication = HttpBasicAuthentication()
)
urlpatterns = patterns('',
  
   url(r'^api/boundary/?$', xml_choice_resource),
    url(r'^api/xml/boundary/?$', xml_choice_resource),
      url(r'^api/boundary/(?P<boundary_id>\d+)/?$', xml_choice_resource),
    url(r'^api/xml/boundary/(?P<boundary_id>\d+)/$', xml_choice_resource),
    url(r'^api/json/boundary/?$', json_choice_resource),
    url(r'^api/json/boundary/?$', json_choice_resource),
    url(r'^api/json/boundary/(?P<boundary_id>\d+)/$', json_choice_resource),
   
)
