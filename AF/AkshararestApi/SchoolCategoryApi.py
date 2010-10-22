from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class SchoolCategoryView(Collection):    
    """ To create new School Category school-category/creator/ """
    def get_entry(self,school_category_id):        
        school_category = School_Category.objects.all(id=school_category_id)          
        return ChoiceEntry(self, school_category)   

template_school_category_view =  SchoolCategoryView(
    queryset = School_Category.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'school_category',        
    ),
  receiver = XMLReceiver(),
)


urlpatterns = patterns('',             
   url(r'^school-category/creator/?$', template_school_category_view.responder.create_form, {'form_class':'school_category'}),   
)
