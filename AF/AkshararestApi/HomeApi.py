from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
from django.template import Template, Context, RequestContext
from schools.forms import *
from schools.models import *
from django_restapi.authentication import *
from django.contrib.auth import authenticate, login, logout

class KLP_Home(Resource):
    """ To generate Home Page home/"""
    def read(self,request):
    	user = request.user    
    	if user.id:
	    	try:
	    		sessionVal = int(request.session['session_sch_typ'])
	    	except:
	    		sessionVal = 0
		respType = request.GET.get('respType') or None
		boundType_List = Boundary_Type.objects.all()
		klp_UserGroups = user.groups.all()
		user_GroupsList = ['%s' %(usergroup.name) for usergroup in klp_UserGroups]
		respDict = {'legend':'Karnataka Learning Partnership ', 'title':'Karnataka Learning Partnership ', 'entry':'Add', 'boundType_List':boundType_List,  'session_sch_typ':sessionVal, 'user':user, 'usergroups':user_GroupsList}
		if respType == None and (user.is_superuser or 'Data Entry Executive' in user_GroupsList or user.is_staff):
		    respDict['home'] = True
		    respDict['urHere'] = 'Home'
		elif respType == 'programme' and (user.is_superuser or user.is_staff):
		    respDict['programme'] = True
		    respDict['urHere'] = 'Programme'
		elif respType == 'filter' and (user.is_superuser or user.is_staff or 'Data Entry Operator' in user_GroupsList or  'Data Entry Executive' in user_GroupsList):
		    respDict['home'] = True    
		    respDict['filter'] = True  
		    respDict['urHere'] = 'Data Entry'
		    respDict['prgsList'] =  Programme.objects.filter(active=2, programme_institution_category=sessionVal)
		elif respType == 'userpermissions' and (user.is_superuser or 'AdminGroup' in user_GroupsList):  
			respDict['home'] = True    
		    	respDict['filter'] = True  
		    	respDict['permission'] = True  
		    	respDict['urHere'] = 'Permissions'
		    	respDict['prgsList'] =  Programme.objects.filter(active=2, programme_institution_category=sessionVal)
		elif respType == 'createUser' and (user.is_superuser or 'AdminGroup' in user_GroupsList):  
			return HttpResponseRedirect('accounts/auth/user/add/')
		elif respType == 'changepermissions' and (user.is_superuser or 'AdminGroup' in user_GroupsList):  
			return HttpResponseRedirect('change/user/permissions')
		else:
			logout(request)
			return HttpResponseRedirect('/login/')         
			  
		respTemplate = render_to_response("viewtemplates/home.html",respDict)
		return HttpResponse(respTemplate)
	else:
		return HttpResponseRedirect('/login/')


def KLP_Set_Session(request):
	request.session['session_sch_typ'] = request.GET.get('sessionVal')
	return HttpResponse('Success')            
        
urlpatterns = patterns('',             
   url(r'^home/$', KLP_Home(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^set/session/$', KLP_Set_Session),
)        
