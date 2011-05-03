from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from schools.models import *
from django.http import *
from Akshara.AkshararestApi.Treeresponder import *
from django.db.models.query import QuerySet


def hasChild(query, typ, boundaryType, filterBy, secFilter, permFilter, assessmentPerm, shPerm, userSel):
	""" This method checks for child objects and get urls """
    	subboundary = 0
	childtree = 0
	childDic={}
	for i in query:
		if typ == 'source' or typ == 'boundary': 
		    if permFilter:
		    	templist = [i.getPermissionChild(boundaryType), i.getPermissionViewUrl()]
		    elif assessmentPerm:
		    	templist = [i.getPermissionChild(boundaryType), i.getAssessmentPermissionViewUrl(secFilter)]
		    elif shPerm:
		    	templist = [i.getPermissionChild(boundaryType), i.showPermissionViewUrl(userSel)]		
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
	""" This method returns assigned institutions for the user"""
	rawQuerySet = Institution.objects.raw(""" SELECT "id","obj_id" FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = 't' """ %(userId))
	inst_list=[]
	for permObj in rawQuerySet:
		inst_list.append(permObj.obj_id)
	return inst_list
	
def KLP_assignedAssessmentInst(userId, assessmentId):
	""" This method returns assigned Assessments for the user"""
	inst_list = UserAssessmentPermissions.objects.filter(user__id=userId, assessment__id=assessmentId, access=True).values_list("instituion__id", flat=True).distinct()
	return inst_list	

def TreeClass(request):
     model = request.GET['root']
     data = request.GET['home']
     filterBy = request.GET['filter']
     secFilter = request.GET['secFilter']
     boundaryType = request.GET['boundTyp']
     permFilter = request.GET.get('permission')
     assessmentPerm = request.GET.get('assesspermission')
     shPerm = request.GET.get('shPerm')
     userSel = request.GET.get('userSel')
     model = model.split('_')
     typ = model[0]
     logUser = request.user
     klp_UserGroups = logUser.groups.all()
     user_GroupsList = ['%s' %(usergroup.name) for usergroup in klp_UserGroups]
     if typ == "source":
     	# if type is source
	if data:
	    # if home is true query for boundaries		
	    if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList) and filterBy == 'None':
	    	# if logged in user is super user or staff or in AdminGroup and filterBy is none query all active boundary's where parent is 1 and based on boundaryType
	    	query = Boundary.objects.filter(parent__id=1,active=2, boundary_type=boundaryType).order_by("name").extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
	    else:
	    	if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList) :
	    		# if logged in user is super user or staff or in AdminGroup and filterBy is not none query all active SG's based on assessments
	    		studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
	    		# Query institutions based SG's
	    		institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution__id', flat=True).distinct()
	    	elif filterBy == 'None':
	    		# if user is not superuser and not staff and not related to admin group and filterby is none get all assigned institutions.
	    		institutions_list = KLP_assignedInstitutions(logUser.id)
	    	else:
	    		# else query for institutions based on map Sg's
	    		studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
	    		map_institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution__id', flat=True).distinct()
	    		
	    		institutions_list = list(set(map_institutions_list)&set(KLP_assignedAssessmentInst(logUser.id, secFilter)))
	        try:
	        	boundary_list = Boundary.objects.filter(institution__pk__in=institutions_list, active=2, boundary_type=boundaryType).values_list('parent__parent__id', flat=True).distinct()
	        except:
	        	boundary_list = Boundary.objects.filter(institution__pk__in=institutions_list, active=2, boundary_type=boundaryType).values_list('parent__id', flat=True).distinct()
	        	
	        query = Boundary.objects.filter(pk__in=boundary_list, active=2, parent__id=1).distinct().extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
		
	else:
		# if data is not true query for all active programmes.
		query = Programme.objects.filter(active=2, programme_institution_category=boundaryType).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
		typ = 'programme'
     else:
     	# typ is not source
	if typ == 'boundary':
		# if typ is boundary Query for sub boundaries or Institutions
		if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList) and filterBy == 'None':
			# if logged in user is super user or staff or in AdminGroup and filterBy is none query all active boundary's where parent is 1 and based on boundaryType
			query = Boundary.objects.filter(parent__id=model[1], active=2, boundary_type=boundaryType).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
		else:
			if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList):
				# if logged in user is super user or staff or in AdminGroup and filterBy is not none query all active SG's based on assessments
				studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
				# Query institutions based SG's
				institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
			elif filterBy == 'None':
				# if user is not superuser and not staff and not related to admin group and filterby is none get all assigned institutions.
				institutions_list = KLP_assignedInstitutions(logUser.id)
			else:
				# else query for institutions based on map Sg's
				studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
				map_institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
				institutions_list = list(set(map_institutions_list)&set(KLP_assignedAssessmentInst(logUser.id, secFilter)))
				
			parentBoundary = Boundary.objects.get(id=model[1])
			if parentBoundary.boundary_category.boundary_category in ['district',]:
				# Query for Boundaries based on institutions
				boundary_list = Boundary.objects.filter(institution__pk__in=institutions_list, active=2, boundary_type=boundaryType).values_list('parent', flat=True).distinct()
				query = Boundary.objects.filter(parent__id=model[1], pk__in = boundary_list, active=2, boundary_type=boundaryType).distinct().extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
			else:
				boundaries = Boundary.objects.filter(parent__id=model[1], institution__pk__in=institutions_list, active=2, boundary_type=boundaryType).values_list('id', flat=True).distinct()
				query = Boundary.objects.filter(id__in=boundaries).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")	
			
		
		if not query:
			# If Query is Empty Query for Institutions under boundary
			if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList) and filterBy == 'None':
				# if logged in user is super user or staff or in AdminGroup and filterBy is none query all active institutions's based on boundary
				query = Institution.objects.filter(boundary__id=model[1],active=2).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")	
				typ = 'sch'
			else:
				if (logUser.is_superuser or logUser.is_staff or 'AdminGroup' in user_GroupsList):
					# if logged in user is super user or staff or in AdminGroup and filterBy is not none query all active SG's based on assessments
					studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
					institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
					
				elif filterBy == 'None':
					# if user is not superuser and not staff and not related to admin group and filterby is none get all assigned institutions.
					institutions_list = KLP_assignedInstitutions(logUser.id)
				else:
					# else query for institutions based on map Sg's
					studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
					map_institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
					institutions_list = list(set(map_institutions_list)&set(KLP_assignedAssessmentInst(logUser.id, secFilter)))
				
				query = Institution.objects.filter(pk__in=institutions_list, boundary__id=model[1], active=2).distinct().extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
				typ = 'sch'
			
				
	elif typ == 'programme':
		# if typ is programme Query For active assessment based On programme id
		query = Assessment.objects.filter(programme__id=model[1],active=2).extra(select={'lower_name':'lower(name)'}).order_by("lower_name")
	elif typ == 'assessment':
		# if typ is assessment Query For active Questions based On assessment id
		query = Question.objects.filter(assessment__id=model[1],active=2)	
	else:
		if typ == 'institution':
			# if typ is Institution Query For active Sgs 
			if filterBy != 'None':
				
				studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=secFilter, active=2).values_list('student_group', flat=True).distinct()
				query = StudentGroup.objects.filter(institution__id = model[1], active=2, id__in=studentgroup_list).distinct().extra(select={'lower_class': 'lower(name)'}).order_by("lower_class","section")
			else:
		  		query = StudentGroup.objects.filter(institution__id = model[1], active=2).extra(select={'lower_class': 'lower(name)'}).order_by("lower_class","section")
		  
   
     CDict=hasChild(query, typ, boundaryType, filterBy, secFilter, permFilter, assessmentPerm, shPerm, userSel)  # Checking for child objects
     val= Collection(
     queryset = query,
     responder = TreeResponder(CDict=CDict),
     )
     return HttpResponse(val(request),mimetype="application/json")


urlpatterns = patterns('',
   url(r'^tree/$', TreeClass),
)


