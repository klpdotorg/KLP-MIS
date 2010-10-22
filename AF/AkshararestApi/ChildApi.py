from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection, Entry, reverse
from django_restapi.responder import *
from schools.models import Child
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

def getStudentSearch(request):

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
	'''paths=request.path.split('/')
	child_name=paths[-1]
	field_name=paths[len(paths)-2]'''

	fieldName = request.GET['fieldName']
	searchtext = request.GET['searchtext']
	section = request.GET['section']
	queryset = []
	if fieldName=='name':
		queryset=student.objects.filter(name__firstName__startswith=searchtext, class_section__id = section,active = True)

	if fieldName=='dobyear':
		queryset=student.objects.filter(name__dob__year=searchtext, class_section__id = section,active = True)

	if fieldName=='dob':
		child_year=searchtext[0:4]+'-'+searchtext[4:6]+'-'+searchtext[6:8]
		queryset=student.objects.filter(name__dob=searchtext, class_section__id = section,active = True)

	if fieldName=='gender':
		queryset=student.objects.filter(name__gender__startswith=searchtext, class_section__id = section,active = True)

	if fieldName=='mt':
		queryset=student.objects.filter(name__mt__name__startswith=searchtext, class_section__id = section,active = True)

	if fieldName=='mother':
		queryset=student.objects.filter(name__mother__startswith=searchtext, class_section__id = section,active = True)

	if fieldName=='father':
		queryset=student.objects.filter(name__father__startswith=searchtext, class_section__id = section,active = True)

	val=Collection(queryset,
	permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),

	responder = TemplateResponder(
	paginate_by = 1,
	template_dir = 'viewtemplates',
	template_object_name = 'child'
	),
	entry_class = ChoiceEntry,
	#authentication = HttpBasicAuthentication()
	)
	return HttpResponse(val(request))

def Pagination(request):
	''' To display the Child details according to Pagination'''

	section = request.GET['section']
	'''page_no = request.GET['pagination']
	page_no = int(page_no) * 1
	page_next = int(page_no) * 2'''
	queryset = []
	
	queryset=student.objects.filter(class_section__id = section,active = True)  #[page_no:page_next]

	val=Collection(queryset,
	permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),

	responder = TemplateResponder(
	paginate_by = 1,
	template_dir = 'viewtemplates',
	template_object_name = 'child'
	),
	entry_class = ChoiceEntry,
	#authentication = HttpBasicAuthentication()
	)
	return HttpResponse(val(request))

class ChildCollectionentryByName(Collection):

    def read(self, request):
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
	'''paths=request.path.split('/')
	child_name=paths[-1]
	field_name=paths[len(paths)-2]'''

	fieldName = request.GET['fieldName']
	searchtext = request.GET['searchtext']
	section = request.GET['section']
	queryset = []
	if fieldName=='name':
		queryset=student.objects.filter(name__firstName__startswith=searchtext, class_section__id = section)

	if fieldName=='dobyear':
		queryset=student.objects.filter(name__dob__year=searchtext, class_section__id = section)

	if fieldName=='dob':
		child_year=searchtext[0:4]+'-'+searchtext[4:6]+'-'+searchtext[6:8]
		queryset=student.objects.filter(name__dob=searchtext, class_section__id = section)

	if fieldName=='gender':
		queryset=student.objects.filter(name__gender__startswith=searchtext, class_section__id = section)

	if fieldName=='mt':
		queryset=student.objects.filter(name__mt__name__startswith=searchtext, class_section__id = section)

	if fieldName=='mother':
		queryset=student.objects.filter(name__mother__startswith=searchtext, class_section__id = section)

	if fieldName=='father':
		queryset=student.objects.filter(name__father__startswith=searchtext, class_section__id = section)
	filtered_set = self.queryset._clone()
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
    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'child'
    ),
    entry_class = ChoiceEntry,
     authentication = HttpBasicAuthentication()
)

def GetChoices(request):
	data = request.GET['id']
	Id = data.split('_')[-1]
	fieldName = data.split('_')[0]
	json = {}
	if fieldName == 'mt':
		languages = Moi_Type.objects.all()
		for language in languages:
			json[str(language.id)] = str(language.name)
	return json
class ChildUpdate(Resource):    
    def create(self, request):
	data = request.POST['id']
	value = request.POST['value']
	child_id = data.split('_')[-1]
	fieldName = data.split('_')[0]
        childObj = Child.objects.get(id=child_id)
	childObj.__setattr__(fieldName, value)
        childObj.save()
        return HttpResponse(value)   

urlpatterns = patterns('',
    
   url(r'^api/child/?$', xml_choice_resource),
   url(r'^api/xml/child/?$', xml_choice_resource),
   url(r'^api/json/child/?$', json_choice_resource),
   url(r'^api/child/(?P<child_id>\d+)/?$', xml_choice_resourceentry),
   url(r'^api/xml/child/(?P<child_id>\d+)/?$', xml_choice_resourceentry),
   url(r'^api/json/child/(?P<child_id>\d+)/?$', json_choice_resourceentry),
   url(r'^api/child/(?P<field_name>\w+)/(?P<child_name>\w+)/?$', xml_choice_resourceentrybyname, {'is_entry':False}),
   url(r'^api/xml/child/(?P<field_name>\w+)/(?P<child_name>\w+)/?$', xml_choice_resourceentrybyname, {'is_entry':False}),
   url(r'^search/child/?$', getStudentSearch),
   url(r'^pagination/?$', Pagination),
   url(r'^update/child/$', ChildUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^getchoices/$', GetChoices),
   
)
