"""
ConsoleApi is used to run raw sql queries from frontend.
"""
from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry
from django.template import RequestContext
#from pysqlite2 import dbapi2 as sqlite
import psycopg2
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from klp.settings import *

from django.db import transaction
def KLP_Admin_Console(request):
	''' To show the admin Console to run SQl Queries '''
	# get logged in user
	user = request.user
	respDict = {'title':'Karnataka Learning Partnership ', 'user':user}
	# render admin console template
	respTemplate = render_to_response("viewtemplates/admin_console.html", respDict)
	return HttpResponse(respTemplate)
@csrf_exempt      
def KLP_Run_Query(request):  
    ''' To run SQl Queries Entered by admin'''
    # get query to perform 
    adminQuery = request.POST.get('form-klp-query')
    #connection = sqlite.connect('/home/klp/klp/klp.db')
    # Establish connection with postgresql by passing dbname, user name and password.
    d=DATABASES['default']
    datebase=d['NAME']
    user=d['USER']
    password=d['PASSWORD']
    connection = psycopg2.connect(database=datebase, user=user, password=password)
    cursor = connection.cursor()
    isExecute = False
    if adminQuery:
	    try:
	    	# execute query
	    	cursor.execute(adminQuery)
                #                transaction.commit_unless_managed()
	    	# If query executes fine return response as "Query Executed Sucessfully"
                connection.commit()    
	    	respStr = "Query Executed Sucessfully ."
	    	isExecute = True
	    except:
	    	# else return response as "Query You Written May Incorrect, Please Check It"
	    	respStr = "Query You Written May Incorrect, Please Check It."
    else:	
    	# If query is empty return response as "Query You Send Is Empty"
    	respStr = "Query You Send Is Empty"
    # close connection
    cursor.close()
    respDict = {"respStr":respStr, "isExecute":isExecute}
    return HttpResponse(simplejson.dumps(respDict), content_type='application/json; charset=utf-8')
      

urlpatterns = patterns('',             
   url(r'^console/?$', KLP_Admin_Console), 
   url(r'^run-query/?$', KLP_Run_Query),   
)
