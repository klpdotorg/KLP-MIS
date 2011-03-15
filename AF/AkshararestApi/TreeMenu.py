from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from schools.models import *
from django.http import *
from Akshara.AkshararestApi.Treeresponder import *
from django.db.models.query import QuerySet
#from django_restapi.authentication import *
def hasChild(query, typ, boundaryType, filterBy, secFilter, permFilter, assessmentPerm):
    	subboundary = 0
	childtree = 0
	childDic={}
	for i in query:
		if typ == 'source' or typ == 'boundary': 
		    if permFilter:
		    	templist = [i.getPermissionChild(boundaryType), i.getPermissionViewUrl()]
		    elif assessmentPerm:
		    	templist = [i.getPermissionChild(boundaryType), i.getAssessmentPermissionViewUrl(secFilter)]	
		    else:
		    	templist = [i.getChild(boundaryType), i.getViewUrl(boundaryType)]
		elif  typ == 'institution' and filterBy != 'None' and permFilter in ['', ' ', None]:
			templist = [i.getChild(),i.getStudentProgrammeUrl(filterBy, secFilter)]       
		else:
		    templist=[i.getChild(),i.getViewUrl()]
		try:
			templist.append(i.GetName())
		except:
			pass
		childDic[i.getModuleName()+'_'+str(i.id)]=templist
	return childDic

def KLP_assignedInstitutions(userId):
	rawQuerySet = Institution.objects.raw(""" SELECT "id","obj_id" FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = 't' """ %(userId))
	inst_list=[]
	for permObj in rawQuerySet:
		inst_list.append(permObj.obj_id)
	return inst_list
	
def KLP_assignedAssessmentInst(userId, assessmentId):
	inst_list = UserAssessmentPermissions.objects.filter(user__id=userId, assessment__id=assessmentId, access=True).values_list("instituion__id", flat=True).distinct()
	return inst_list	

def SampleClass(request):
     model = request.GET['root']
     data = request.GET['home']
     filterBy = request.GET['filter']
     secFilter = request.GET['secFilter']
     boundaryType = request.GET['boundTyp']
     permFilter = request.GET.get('permission')
     assessmentPerm = request.GET.get('assesspermission')
     model = model.split('_')
     modelObjects = {'source':Boundary,'boundary':Institution,} 
     fields  = {'boundary':Institution,} 
     childs = {}
     typ = model[0]
     logUser = request.user
     klp_UserGroups = logUser.groups.all()
     user_GroupsList = ['%s' %(usergroup.name) for usergroup in klp_UserGroups]
     if model[0] == "source":
	if data:
	    
	    if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList) and filterBy == 'None':
	    	query = Boundary.objects.filter(parent__id=1,active=2, boundary_type=boundaryType).order_by("name").extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
	    else:
	    	if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList) :
	    		studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
	    		institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution__id', flat=True).distinct()
	    	elif filterBy == 'None':
	    		institutions_list = KLP_assignedInstitutions(logUser.id)
	    	else:
	    		studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
	    		map_institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution__id', flat=True).distinct()
	    		
	    		institutions_list = list(set(map_institutions_list)&set(KLP_assignedAssessmentInst(logUser.id, secFilter)))
	        try:
	        	boundary_list = Boundary.objects.filter(institution__pk__in=institutions_list, active=2, boundary_type=boundaryType).values_list('parent__parent__id', flat=True).distinct()
	        except:
	        	boundary_list = Boundary.objects.filter(institution__pk__in=institutions_list, active=2, boundary_type=boundaryType).values_list('parent__id', flat=True).distinct()
	        	
	        query = Boundary.objects.filter(pk__in=boundary_list, active=2, parent__id=1).distinct().extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
		
	else:
		query = Programme.objects.filter(active=2, programme_institution_category=boundaryType).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
		typ = 'programme'
     else:
	if model[0] == 'boundary':
		if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList) and filterBy == 'None':
			query = Boundary.objects.filter(parent__id=model[1], active=2, boundary_type=boundaryType).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
		else:
			if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList):
				studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
				institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
			elif filterBy == 'None':
				institutions_list = KLP_assignedInstitutions(logUser.id)
			else:
				studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
				map_institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
				institutions_list = list(set(map_institutions_list)&set(KLP_assignedAssessmentInst(logUser.id, secFilter)))
				
			parentBoundary = Boundary.objects.get(id=model[1])
			if parentBoundary.boundary_category.boundary_category in ['district',]:
				boundary_list = Boundary.objects.filter(institution__pk__in=institutions_list, active=2, boundary_type=boundaryType).values_list('parent', flat=True).distinct()
				query = Boundary.objects.filter(parent__id=model[1], pk__in = boundary_list, active=2, boundary_type=boundaryType).distinct().extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
			else:
				boundaries = Boundary.objects.filter(parent__id=model[1], institution__pk__in=institutions_list, active=2, boundary_type=boundaryType).values_list('id', flat=True).distinct()
				query = Boundary.objects.filter(id__in=boundaries).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")	
			
		
		if not query:
			if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList) and filterBy == 'None':
				query = Institution.objects.filter(boundary__id=model[1],active=2).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")	
				typ = 'sch'
			else:
				if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList):
					studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
					institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
					
				elif filterBy == 'None':
					institutions_list = KLP_assignedInstitutions(logUser.id)
				else:
					studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
					map_institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
					institutions_list = list(set(map_institutions_list)&set(KLP_assignedAssessmentInst(logUser.id, secFilter)))
				
				query = Institution.objects.filter(pk__in=institutions_list, boundary__id=model[1], active=2).distinct().extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
				typ = 'sch'
			
				
	elif model[0] == 'programme':
		query = Assessment.objects.filter(programme__id=model[1],active=2).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
	elif model[0] == 'assessment':
		query = Question.objects.filter(assessment__id=model[1],active=2)	
	else:
		if model[0] == 'institution':
			if filterBy != 'None':
				
				studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
				query = StudentGroup.objects.filter(institution__id = model[1], active=2, id__in=studentgroup_list).distinct().extra(select={'lower_class': 'lower(name)'}).order_by("lower_class","section")
			else:
		  		query = StudentGroup.objects.filter(institution__id = model[1], active=2).extra(select={'lower_class': 'lower(name)'}).order_by("lower_class","section")
		if model[0] == 'studentgroup':
		  query = Student.objects.filter(student_group__id=model[1],active=2)
		  

     CDict=hasChild(query, typ, boundaryType, filterBy, secFilter, permFilter, assessmentPerm)
     val= Collection(
     queryset = query,
     responder = TreeResponder(CDict=CDict),
     )
     return HttpResponse(val(request),mimetype="application/json")
#authentication = HttpBasicAuthentication()           
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


