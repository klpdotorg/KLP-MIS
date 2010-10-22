from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from schools.models import *
from django.http import *
from Akshara.AkshararestApi.Treeresponder import *
from django.db.models.query import QuerySet
def hasChild(query, typ, filterBy):
    	subboundary = 0
	childtree = 0
	childDic={}
	for i in query:
		if typ == 'class' and filterBy != 'None':
		    templist=[i.getChild(),i.getStudentProgrammeUrl(filterBy),i.getEditUrl(),i.getDeleteUrl()]
		else:
		    templist=[i.getChild(),i.getViewUrl(),i.getEditUrl(),i.getDeleteUrl()]
		try:
			templist.append(i.GetName())
		except:
			pass
		childDic[i.getModuleName()+'_'+str(i.id)]=templist
	return childDic


def SampleClass(request):
     model = request.GET['root']
     data = request.GET['home']
     filterBy = request.GET['filter']
     model = model.split('_')
     modelObjects = {'source':Boundary,'boundary':School,"school":Class,'class':Sections,'sections':student}
     fields  = {'boundary':School,'schools':Class,'class':Sections,'sections':student}
     childs = {}
     if model[0] == "source":
	if data:
	    
	    if filterBy != 'None':
	        query = []
	        students_list = Answer.objects.filter(assessmentDetail__assessment__programme__id=filterBy).values_list('student',flat=True).distinct('student')
	        
	        #boundary_list = Boundary.objects.filter(school__class__sections__student__pk__in=students_list).distinct()
	        #print boundary_list
	        #t1=Boundary.objects.filter(school__class__sections__student__pk__in=students_list).values_list('id',flat=True).distinct()
	        #print  t1,Boundary.objects.filter(parent__id__in=t1),'test'
	        #query = Boundary.objects.filter(boundary__parent__in=boundary_list, parent__id=1)
	        query = Boundary.objects.filter(school__class__sections__student__pk__in=students_list).distinct()
	        #print query
	    else:
		    query = Boundary.objects.filter(parent__id=1,active=True)
		    
		
	else:
		query = Programme.objects.filter(active=True)
     else:
	if model[0] == 'boundary':
     		query = Boundary.objects.filter(parent__id=model[1],active=True)
		#print "boundary",query
		if not query:
			query = School.objects.filter(boundary__id=model[1],active=True)
	elif model[0] == 'programme':
		query = Assessment.objects.filter(programme__id=model[1],active=True)
	elif model[0] == 'assessment':
		query = AssessmentDetail.objects.filter(assessment__id=model[1],active=True)		
	else:
		if model[0] == 'school':
		  query = Class.objects.filter(sid__id=model[1],active=True)
		if model[0] == 'class':
		  query = Sections.objects.filter(classname__id=model[1],active=True,)
		if model[0] == 'sections':
		  query = student.objects.select_related().filter(class_section__id=model[1],active=True)

     CDict=hasChild(query,model[0], filterBy)
     val= Collection(
     queryset = query,
     responder = TreeResponder(CDict=CDict)
     )
     return HttpResponse(val(request),mimetype="application/json")
           
xml_poll_resource = Collection(
    queryset = Boundary.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    expose_fields = ('id', 'question', 'pub_date'),
    responder = XMLResponder(paginate_by = 10)
)

xml_choice_resource = Collection(
    queryset = Boundary.objects.all(),
    permitted_methods = ('GET',),
    expose_fields = ('id', 'poll_id', 'choice'),
    responder = XMLResponder(paginate_by = 5)
)

urlpatterns = patterns('',
   url(r'^tree/$', SampleClass),
   url(r'^xml/polls/(.*?)/?$', xml_poll_resource),
   url(r'^xml/choices/(.*?)/?$', xml_choice_resource)
)


